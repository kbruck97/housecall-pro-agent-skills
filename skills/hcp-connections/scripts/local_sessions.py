#!/usr/bin/env python3
"""Local, tenant-isolated HCP session bootstrap. No business-operation adapter.

Cookies stay in memory or AES-GCM encrypted local storage. Only the native OS
keyring holds the encryption key. Never add a cookie-export CLI or arbitrary URL.
Identity and cookie names are observed internal contracts, not public HCP APIs.
"""
from __future__ import annotations

import argparse
import base64
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass, field
import http.cookiejar
import json
import logging
import math
import os
from pathlib import Path
import re
import secrets
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid


ORIGIN = "https://pro.housecallpro.com"
IDENTITY_URL = ORIGIN + "/alpha/pro"
SESSION_COOKIE = "_housecall-web_session_with_domain"
ALLOWED_COOKIES = frozenset((SESSION_COOKIE, "csrf_token"))
SERVICE = "TSM.HousecallPro.local-session.v1"
MAX_SECRET_BYTES = 24_576
MAX_RESPONSE_BYTES = 262_144
RETENTION_SECONDS = 30 * 24 * 60 * 60
REQUEST_TIMEOUT = 15
SAFE_MESSAGES = {
    "missing": "No saved connection. Run connect to sign in locally.",
    "expired": "Saved authentication expired. Run connect to sign in again.",
    "forbidden": "HCP denied access. Resolve permissions; do not change accounts to bypass denial.",
    "wrong_company": "The authenticated company differs from the trusted expected company. Nothing was saved.",
    "network_error": "The identity request could not complete. Saved authentication was retained.",
    "redirect": "Identity returned a redirect. Diagnose the login contract before reconnecting.",
    "invalid_response": "Identity did not match the observed JSON contract. Saved authentication was retained.",
    "storage_error": "Protected local storage is unavailable or invalid. No plaintext fallback is permitted.",
    "unsupported_platform": "This helper supports native Windows Credential Manager and macOS Keychain only.",
    "dependencies_missing": "Install this skill's optional runtime dependencies and Playwright Chromium.",
    "invalid_company": "Supply the trusted HCP company UUID from configuration or a verified public API response.",
    "invalid_cookie": "The session cookie contract is unsupported. No authentication was saved.",
    "login_timeout": "Login did not complete within the time limit. Nothing new was saved.",
    "login_cancelled": "The dedicated login window was closed. Nothing new was saved.",
    "browser_error": "The dedicated login browser could not complete. Check its installation and login access.",
    "unsafe_debug": "Disable Playwright debug/trace environment settings before handling authentication.",
    "busy": "Another operation is already using this company's local connection. Retry after it finishes.",
}


class SessionError(Exception):
    """Only fixed safe text escapes the helper; never include upstream exceptions."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(SAFE_MESSAGES[code])


def company_id(value: str) -> str:
    try:
        parsed = str(uuid.UUID(value))
        if not isinstance(value, str) or value.lower() != parsed:
            raise ValueError
        return parsed
    except (ValueError, AttributeError, TypeError):
        raise SessionError("invalid_company") from None


def default_root() -> Path:
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA")
        if not base or not Path(base).is_absolute():
            raise SessionError("storage_error")
        return Path(base) / "TSM" / "HousecallPro"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "TSM" / "HousecallPro"
    raise SessionError("unsupported_platform")


def native_keyring():
    """Choose an exact backend, never a configurable/plaintext/chained fallback."""
    try:
        if sys.platform == "win32":
            from keyring.backends.Windows import WinVaultKeyring
            backend = WinVaultKeyring()
            backend.persist = "local machine"  # Never the enterprise-roaming default.
        elif sys.platform == "darwin":
            from keyring.backends.macOS import Keyring
            backend = Keyring()
            backend.keychain = None  # Do not use an environment-selected keychain.
        else:
            raise SessionError("unsupported_platform")
        if backend.priority <= 0:
            raise SessionError("storage_error")
        return backend
    except ImportError:
        raise SessionError("dependencies_missing") from None
    except SessionError:
        raise
    except Exception:
        raise SessionError("storage_error") from None


def filter_cookies(raw: list[dict], *, now: float | None = None) -> list[dict]:
    """Retain only observed names on the exact app host and narrow their scope."""
    now = time.time() if now is None else now
    if not isinstance(raw, list) or len(raw) > 512:
        raise SessionError("invalid_cookie")
    found = {}
    for item in raw:
        if not isinstance(item, dict) or item.get("name") not in ALLOWED_COOKIES:
            continue
        if item.get("domain") not in ("pro.housecallpro.com", ".pro.housecallpro.com"):
            continue
        name, value = item["name"], item.get("value")
        expires = item.get("expires", -1)
        if (not isinstance(value, str) or not value or len(value) > 16_384
                or re.search(r"[\x00-\x20\x7f;]", value)
                or item.get("path") != "/" or type(item.get("secure")) is not bool
                or (name == SESSION_COOKIE and item["secure"] is not True)
                or type(expires) not in (int, float) or not math.isfinite(expires)):
            raise SessionError("invalid_cookie")
        if expires != -1 and expires <= now:
            continue
        if name in found:
            raise SessionError("invalid_cookie")
        found[name] = {"name": name, "value": value, "domain": "pro.housecallpro.com",
                       "path": "/", "expires": expires, "secure": True,
                       "httpOnly": bool(item.get("httpOnly", False)),
                       "sameSite": item.get("sameSite") if item.get("sameSite") in
                       ("Strict", "Lax", "None") else "Lax"}
    if SESSION_COOKIE not in found:
        raise SessionError("expired")
    return [found[name] for name in sorted(found)]


@dataclass(repr=False)
class VerifiedSession:
    """In-process handle for a separately reviewed adapter; never JSON-export it.

    This object proves identity only at verified_at. It does not authorize an HCP
    operation, establish its route/CSRF schema, or confer permission to write.
    """

    company_id: str
    cookies: list[dict] = field(repr=False)
    created_at: float
    verified_at: float


class LocalStore:
    def __init__(self, root: Path | None = None, backend=None):
        self.root = default_root() if root is None else Path(root)
        self.backend = native_keyring() if backend is None else backend
        self._cipher(b"\x00" * 32)  # Detect missing encryption support before prompting for login.

    def _paths(self, expected: str):
        folder = self.root / company_id(expected)
        if self.root.is_symlink() or folder.is_symlink():
            raise SessionError("storage_error")
        return folder, folder / "session.enc", folder / "metadata.json"

    @contextmanager
    def transaction(self, expected: str):
        """One active operation per local tenant, including bounded interactive login."""
        folder, _, _ = self._paths(expected)
        descriptor = None
        locked = False
        try:
            folder.mkdir(mode=0o700, parents=True, exist_ok=True)
            if os.name != "nt":
                self.root.chmod(0o700)
                folder.chmod(0o700)
            lock = folder / ".connection.lock"
            if lock.is_symlink():
                raise SessionError("storage_error")
            descriptor = os.open(lock, os.O_CREAT | os.O_RDWR, 0o600)
            if os.fstat(descriptor).st_size == 0:
                os.write(descriptor, b"0")
            os.lseek(descriptor, 0, os.SEEK_SET)
            try:
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(descriptor, msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                locked = True
            except OSError:
                raise SessionError("busy") from None
            yield
        except SessionError:
            raise
        except OSError:
            raise SessionError("storage_error") from None
        finally:
            if descriptor is not None:
                try:
                    if locked:
                        if os.name == "nt":
                            import msvcrt
                            os.lseek(descriptor, 0, os.SEEK_SET)
                            msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
                        else:
                            import fcntl
                            fcntl.flock(descriptor, fcntl.LOCK_UN)
                finally:
                    os.close(descriptor)

    def _key(self, expected: str, *, create: bool = False) -> bytes | None:
        try:
            name = SERVICE + "." + expected
            encoded = self.backend.get_password(name, expected)
            if encoded is None and create:
                encoded = base64.b64encode(secrets.token_bytes(32)).decode("ascii")
                self.backend.set_password(name, expected, encoded)
                if self.backend.get_password(name, expected) != encoded:
                    raise SessionError("storage_error")
            if encoded is None:
                return None
            key = base64.b64decode(encoded, validate=True)
            if len(key) != 32:
                raise SessionError("storage_error")
            return key
        except Exception:
            raise SessionError("storage_error") from None

    @staticmethod
    def _cipher(key: bytes):
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            return AESGCM(key)
        except ImportError:
            raise SessionError("dependencies_missing") from None

    @staticmethod
    def _atomic(path: Path, data: bytes):
        temporary = None
        try:
            if path.is_symlink():
                raise SessionError("storage_error")
            fd, temporary = tempfile.mkstemp(prefix=".session-", dir=path.parent)
            with os.fdopen(fd, "wb") as stream:
                if os.name != "nt":
                    os.fchmod(stream.fileno(), 0o600)
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            if temporary and os.path.exists(temporary):
                os.unlink(temporary)

    def load(self, expected: str) -> VerifiedSession | None:
        expected = company_id(expected)
        try:
            _, encrypted, _ = self._paths(expected)
            if not encrypted.exists():
                return None
            if encrypted.is_symlink() or encrypted.stat().st_size > MAX_SECRET_BYTES + 64:
                raise SessionError("storage_error")
            key = self._key(expected)
            if key is None:
                raise SessionError("storage_error")
            payload = encrypted.read_bytes()
            if len(payload) < 29 or len(payload) > MAX_SECRET_BYTES + 64:
                raise SessionError("storage_error")
            raw = self._cipher(key).decrypt(payload[:12], payload[12:], (SERVICE + expected).encode())
            record = json.loads(raw)
            if (record.get("version") != 1 or record.get("company_id") != expected
                    or type(record.get("created_at")) not in (int, float)
                    or type(record.get("verified_at")) not in (int, float)
                    or not math.isfinite(record["created_at"])
                    or not math.isfinite(record["verified_at"])):
                raise SessionError("storage_error")
            now = time.time()
            if record["created_at"] > now + 60 or record["verified_at"] > now + 60:
                raise SessionError("storage_error")
            if now - record["created_at"] >= RETENTION_SECONDS:
                raise SessionError("expired")
            return VerifiedSession(expected, filter_cookies(record["cookies"], now=now),
                                   record["created_at"], record["verified_at"])
        except SessionError:
            raise
        except Exception:
            raise SessionError("storage_error") from None

    def save(self, session: VerifiedSession):
        expected = company_id(session.company_id)
        try:
            cookies = filter_cookies(session.cookies)
            record = {"version": 1, "company_id": expected, "cookies": cookies,
                      "created_at": session.created_at, "verified_at": session.verified_at}
            raw = json.dumps(record, separators=(",", ":"), allow_nan=False).encode()
            if len(raw) > MAX_SECRET_BYTES:
                raise SessionError("storage_error")
            folder, encrypted, metadata = self._paths(expected)
            folder.mkdir(mode=0o700, parents=True, exist_ok=True)
            if os.name != "nt":
                self.root.chmod(0o700)
                folder.chmod(0o700)
            key = self._key(expected, create=True)
            nonce = secrets.token_bytes(12)
            payload = nonce + self._cipher(key).encrypt(nonce, raw, (SERVICE + expected).encode())
            self._atomic(encrypted, payload)
            # This file contains identifiers/timestamps only, never response bodies or secrets.
            public = {"version": 1, "company_id": expected,
                      "created_at": session.created_at, "verified_at": session.verified_at,
                      "local_expires_at": session.created_at + RETENTION_SECONDS,
                      "secret_storage": "AES-GCM; key held by native OS keyring"}
            self._atomic(metadata, json.dumps(public, indent=2).encode())
        except SessionError:
            raise
        except Exception:
            raise SessionError("storage_error") from None

    def forget(self, expected: str):
        expected = company_id(expected)
        with self.transaction(expected):
            self._forget(expected)

    def _forget(self, expected: str):
        try:
            folder, encrypted, metadata = self._paths(expected)
            for path in (encrypted, metadata):
                if path.is_symlink():
                    raise SessionError("storage_error")
            # Delete key first so any leftover ciphertext cannot be used by this helper.
            if self.backend.get_password(SERVICE + "." + expected, expected) is not None:
                self.backend.delete_password(SERVICE + "." + expected, expected)
            encrypted.unlink(missing_ok=True)
            metadata.unlink(missing_ok=True)
            if folder.exists() and not any(folder.iterdir()):
                folder.rmdir()
        except SessionError:
            raise
        except Exception:
            raise SessionError("storage_error") from None


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class PinnedCookieJar(http.cookiejar.CookieJar):
    def set_cookie(self, cookie, *args, **kwargs):
        if (cookie.name not in ALLOWED_COOKIES
                or cookie.domain not in ("pro.housecallpro.com", ".pro.housecallpro.com")):
            return
        # Host-only and .pro cookies are the same narrowly pinned credential here.
        # Canonicalize Set-Cookie rotation so an older value cannot shadow its update.
        cookie.domain = "pro.housecallpro.com"
        cookie.domain_specified = False
        cookie.domain_initial_dot = False
        return super().set_cookie(cookie, *args, **kwargs)


def _jar(cookies: list[dict]) -> http.cookiejar.CookieJar:
    jar = PinnedCookieJar()
    for item in filter_cookies(cookies):
        expires = None if item["expires"] == -1 else int(item["expires"])
        jar.set_cookie(http.cookiejar.Cookie(
            0, item["name"], item["value"], None, False, "pro.housecallpro.com", False,
            False, "/", True, True, expires, expires is None, None, None,
            {"HttpOnly": None} if item["httpOnly"] else {}, False))
    return jar


def _jar_cookies(jar) -> list[dict]:
    return filter_cookies([{"name": c.name, "value": c.value, "domain": c.domain,
                           "path": c.path, "secure": c.secure,
                           "expires": -1 if c.expires is None else c.expires,
                           "httpOnly": c.has_nonstandard_attr("HttpOnly")}
                          for c in jar])


def verify_identity(cookies: list[dict], expected: str) -> list[dict]:
    """The sole network operation: fixed HTTPS GET, no retries or redirects."""
    expected = company_id(expected)
    jar = _jar(cookies)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect(),
                                       urllib.request.HTTPCookieProcessor(jar))
    request = urllib.request.Request(IDENTITY_URL, headers={"Accept": "application/json"}, method="GET")
    try:
        with opener.open(request, timeout=REQUEST_TIMEOUT) as response:
            if response.status != 200:
                raise SessionError("invalid_response")
            if response.headers.get_content_type() != "application/json":
                raise SessionError("invalid_response")
            body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                raise SessionError("invalid_response")
        record = json.loads(body)
        if not isinstance(record, dict) or not isinstance(record.get("organization_uuid"), str):
            raise SessionError("invalid_response")
        try:
            actual = company_id(record["organization_uuid"])
        except SessionError:
            raise SessionError("invalid_response") from None
        if actual != expected:
            raise SessionError("wrong_company")
        return _jar_cookies(jar)
    except urllib.error.HTTPError as error:
        code = ("expired" if error.code == 401 else "forbidden" if error.code == 403
                else "redirect" if 300 <= error.code < 400 else "invalid_response")
        error.close()
        raise SessionError(code) from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise SessionError("network_error") from None
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise SessionError("invalid_response") from None


def interactive_login(expected: str, timeout: int = 300) -> list[dict]:
    """User performs official login/MFA; the agent never receives login fields."""
    expected = company_id(expected)
    if not 30 <= timeout <= 600:
        raise SessionError("login_timeout")
    if any(os.environ.get(name) for name in ("DEBUG", "PWDEBUG", "PW_TRACE", "PW_TEST_TRACE")):
        raise SessionError("unsafe_debug")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SessionError("dependencies_missing") from None
    print("Sign in to the intended company in the dedicated Housecall Pro window and complete MFA. "
          "Enter credentials only on the official website, never in chat. Close the window to cancel.", flush=True)
    deadline = time.monotonic() + timeout
    try:
        with sync_playwright() as runtime:
            browser = runtime.chromium.launch(headless=False)
            try:
                context = browser.new_context()
                page = context.new_page()
                page.goto(ORIGIN, wait_until="domcontentloaded", timeout=30_000)
                while time.monotonic() < deadline:
                    if not browser.is_connected() or not context.pages:
                        raise SessionError("login_cancelled")
                    try:
                        candidate = filter_cookies(context.cookies(IDENTITY_URL))
                        # Verify only the narrow cookie jar; browser cookies never become a generic client.
                        return verify_identity(candidate, expected)
                    except SessionError as error:
                        if error.code != "expired":
                            raise
                    # Playwright's event loop remains responsive to window closure.
                    context.pages[0].wait_for_timeout(1500)
                raise SessionError("login_timeout")
            except SessionError:
                raise
            except Exception:
                if not browser.is_connected() or not context.pages:
                    raise SessionError("login_cancelled") from None
                raise
            finally:
                if browser.is_connected():
                    browser.close()
    except SessionError:
        raise
    except Exception:
        raise SessionError("browser_error") from None


class SessionManager:
    def __init__(self, store, verifier=verify_identity, login=interactive_login):
        self.store, self.verifier, self.login = store, verifier, login

    def status(self, expected: str) -> VerifiedSession:
        expected = company_id(expected)
        with self.store.transaction(expected) if hasattr(self.store, "transaction") else nullcontext():
            return self._status(expected)

    def _status(self, expected: str) -> VerifiedSession:
        saved = self.store.load(expected)
        if saved is None:
            raise SessionError("missing")
        if saved.company_id != expected:
            raise SessionError("wrong_company")
        cookies = self.verifier(saved.cookies, expected)
        current = VerifiedSession(expected, cookies, saved.created_at, time.time())
        self.store.save(current)  # Persist rotated cookies only after verified identity.
        return current

    def connect(self, expected: str, timeout: int = 300) -> VerifiedSession:
        expected = company_id(expected)
        with self.store.transaction(expected) if hasattr(self.store, "transaction") else nullcontext():
            return self._connect(expected, timeout)

    def _connect(self, expected: str, timeout: int) -> VerifiedSession:
        try:
            return self._status(expected)
        except SessionError as error:
            if error.code not in ("missing", "expired"):
                raise
        cookies = self.login(expected, timeout)
        # Recheck independently of the login callback before persistence.
        cookies = self.verifier(cookies, expected)
        now = time.time()
        current = VerifiedSession(expected, cookies, now, now)
        self.store.save(current)
        return current


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Connect one HCP company using a protected local web session.")
    parser.add_argument("command", choices=("status", "connect", "forget"))
    parser.add_argument("--company-id", required=True, help="Trusted expected HCP organization UUID; never a guessed label")
    parser.add_argument("--timeout", type=int, default=300, help="Interactive login budget, 30–600 seconds (connect only)")
    args = parser.parse_args(argv)
    # Never allow dependency debug logs to serialize credentials in this process.
    logging.disable(logging.CRITICAL)
    try:
        expected = company_id(args.company_id)
        store = LocalStore()
        if args.command == "forget":
            store.forget(expected)
            output = {"state": "forgotten", "company_id": expected,
                      "note": "Local credentials removed; this does not revoke HCP's server session."}
        else:
            manager = SessionManager(store)
            session = manager.connect(expected, args.timeout) if args.command == "connect" else manager.status(expected)
            output = {"state": "verified", "company_id": session.company_id,
                      "verified_at": session.verified_at, "surface": "observed-internal identity GET",
                      "metadata": str(store.root / expected / "metadata.json")}
        print(json.dumps(output, indent=2))
        return 0
    except SessionError as error:
        print(json.dumps({"state": error.code, "message": str(error)}))
        return 2
    except KeyboardInterrupt:
        print(json.dumps({"state": "login_cancelled", "message": SAFE_MESSAGES["login_cancelled"]}))
        return 2
    except Exception:
        print(json.dumps({"state": "storage_error", "message": SAFE_MESSAGES["storage_error"]}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

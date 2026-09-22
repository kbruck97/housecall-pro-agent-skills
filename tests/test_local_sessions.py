"""Synthetic session-manager regressions; no browser, HCP, or OS vault access."""
import contextlib
import copy
import email.message
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import types
import unittest
from unittest.mock import patch
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/hcp-connections/scripts"))
import local_sessions as sessions

ALPHA = "11111111-1111-4111-8111-111111111111"
BETA = "22222222-2222-4222-8222-222222222222"
SECRET = "synthetic-cookie-never-print-this"


def cookies(value=SECRET):
    return [{"name": sessions.SESSION_COOKIE, "value": value,
             "domain": ".pro.housecallpro.com", "path": "/", "secure": True,
             "httpOnly": True, "expires": -1, "sameSite": "Lax"}]


def connected(company=ALPHA, value=SECRET):
    return sessions.VerifiedSession(company, cookies(value), time.time(), time.time())


class MemoryStore:
    def __init__(self):
        self.records = {}
        self.saves = []

    def load(self, expected):
        return self.records.get(expected)

    def save(self, session):
        self.records[session.company_id] = session
        self.saves.append(session.company_id)


class FakeKeyring:
    def __init__(self):
        self.items = {}

    def get_password(self, service, username):
        return self.items.get((service, username))

    def set_password(self, service, username, password):
        self.items[service, username] = password

    def delete_password(self, service, username):
        self.items.pop((service, username), None)


class ManagerTests(unittest.TestCase):
    def setUp(self):
        self.store = MemoryStore()
        self.logins = []
        self.requests = []

    def login(self, company, timeout):
        self.logins.append(company)
        return cookies()

    def verify(self, jar, company):
        self.requests.append(company)
        return sessions.filter_cookies(jar)

    def manager(self, verifier=None, login=None):
        return sessions.SessionManager(self.store, verifier or self.verify, login or self.login)

    def assert_code(self, code, function, *args):
        with self.assertRaises(sessions.SessionError) as caught:
            function(*args)
        self.assertEqual(caught.exception.code, code)

    def test_missing_status_never_prompts(self):
        self.assert_code("missing", self.manager().status, ALPHA)
        self.assertEqual(self.logins, [])

    def test_first_connection_and_later_tenant_reuse(self):
        manager = self.manager()
        manager.connect(ALPHA)
        manager.connect(BETA)
        manager.connect(ALPHA)
        self.assertEqual(self.logins, [ALPHA, BETA])
        self.assertEqual(self.requests, [ALPHA, BETA, ALPHA])
        self.assertEqual(set(self.store.records), {ALPHA, BETA})

    def test_expired_reauthenticates_once_and_preserves_other_tenant(self):
        self.store.records = {ALPHA: connected(ALPHA, "old"), BETA: connected(BETA, "other")}

        def verify(jar, company):
            if jar[0]["value"] == "old":
                raise sessions.SessionError("expired")
            return self.verify(jar, company)

        other = self.store.records[BETA]
        self.manager(verify).connect(ALPHA)
        self.assertEqual(self.logins, [ALPHA])
        self.assertIs(self.store.records[BETA], other)

    def test_failures_never_start_login_or_replace_saved_session(self):
        for code in ("forbidden", "wrong_company", "network_error", "invalid_response", "redirect", "storage_error"):
            with self.subTest(code=code):
                old = connected()
                self.store.records[ALPHA] = old

                def fail(*_):
                    raise sessions.SessionError(code)

                self.assert_code(code, self.manager(fail).connect, ALPHA)
                self.assertIs(self.store.records[ALPHA], old)
                self.assertEqual(self.logins, [])

    def test_failed_login_preserves_other_tenants_and_old_auth(self):
        self.store.records = {ALPHA: connected(), BETA: connected(BETA)}
        original = dict(self.store.records)

        def expired(*_):
            raise sessions.SessionError("expired")

        def cancelled(*_):
            raise sessions.SessionError("login_cancelled")

        self.assert_code("login_cancelled", self.manager(expired, cancelled).connect, ALPHA)
        self.assertEqual(self.store.records, original)

    def test_login_callback_is_independently_verified_before_save(self):
        def wrong(*_):
            raise sessions.SessionError("wrong_company")

        self.assert_code("wrong_company", self.manager(wrong).connect, ALPHA)
        self.assertEqual(self.store.records, {})

    def test_wrong_loaded_binding_blocks_before_requests(self):
        self.store.records[ALPHA] = connected(BETA)
        self.assert_code("wrong_company", self.manager().connect, ALPHA)
        self.assertEqual(self.requests, [])

    def test_rotated_cookie_is_saved_after_identity_verification(self):
        old = connected()
        self.store.records[ALPHA] = old
        self.manager(lambda *_: cookies("rotated-value")).status(ALPHA)
        current = self.store.records[ALPHA]
        self.assertEqual(current.cookies[0]["value"], "rotated-value")
        self.assertEqual(current.created_at, old.created_at)
        self.assertNotIn(SECRET, repr(current))

    def test_repeated_auth_failure_does_not_loop(self):
        self.store.records[ALPHA] = connected()

        def expired(*_):
            raise sessions.SessionError("expired")

        self.assert_code("expired", self.manager(expired).connect, ALPHA)
        self.assertEqual(self.logins, [ALPHA])
        self.assertEqual(self.store.saves, [])


class CookieAndTransportTests(unittest.TestCase):
    def test_observed_csrf_without_secure_flag_is_narrowed_to_https(self):
        observed_pair = cookies() + [dict(cookies()[0], name="csrf_token", secure=False, httpOnly=False)]
        clean = sessions.filter_cookies(observed_pair)
        self.assertEqual(len(clean), 2)
        self.assertTrue(all(item["secure"] for item in clean))

    def test_cookie_rotation_does_not_leave_old_host_only_value(self):
        jar = sessions._jar(cookies())
        rotated = copy.copy(next(iter(jar)))
        rotated.domain = ".pro.housecallpro.com"
        rotated.domain_specified = True
        rotated.value = "rotated-cookie"
        jar.set_cookie(rotated)
        self.assertEqual(len(list(jar)), 1)
        self.assertEqual(sessions._jar_cookies(jar)[0]["value"], "rotated-cookie")

    def test_only_observed_names_and_origins_retained(self):
        irrelevant = [dict(cookies()[0], domain="evil.example"),
                      dict(cookies()[0], domain=".housecallpro.com"),
                      dict(cookies()[0], name="analytics-id")]
        clean = sessions.filter_cookies(cookies() + irrelevant)
        self.assertEqual(len(clean), 1)
        self.assertEqual(clean[0]["domain"], "pro.housecallpro.com")

    def test_invalid_cookie_data_and_duplicate_fail(self):
        for changes in ({"secure": False}, {"path": "/unexpected"}, {"value": "bad\nheader"},
                        {"value": "bad;header"}, {"expires": float("nan")}, {"value": "x" * 17000}):
            with self.subTest(changes=list(changes)):
                with self.assertRaises(sessions.SessionError):
                    sessions.filter_cookies([dict(cookies()[0], **changes)])
        with self.assertRaises(sessions.SessionError):
            sessions.filter_cookies(cookies() + cookies())

    def test_expired_cookie_not_used(self):
        with self.assertRaises(sessions.SessionError) as caught:
            sessions.filter_cookies([dict(cookies()[0], expires=100)], now=200)
        self.assertEqual(caught.exception.code, "expired")

    def test_company_identifier_cannot_be_a_path(self):
        for value in ("../../other", "tenant-name", None, ALPHA + "/../" + BETA):
            with self.assertRaises(sessions.SessionError):
                sessions.company_id(value)

    def test_redirect_handler_never_follows(self):
        self.assertIsNone(sessions.NoRedirect().redirect_request(None, None, 302, "", {}, "https://evil.example"))

    def response(self, body, content_type="application/json"):
        class Response:
            status = 200
            headers = email.message.Message()

            def read(self, limit):
                return body[:limit]

            def __enter__(self):
                return self

            def __exit__(self, *_):
                pass

        response = Response()
        response.headers["Content-Type"] = content_type
        return response

    def test_pinned_identity_request_and_schema(self):
        class Opener:
            def open(inner, request, timeout):
                self.assertEqual(request.full_url, sessions.IDENTITY_URL)
                self.assertEqual(request.get_method(), "GET")
                self.assertEqual(timeout, sessions.REQUEST_TIMEOUT)
                return self.response(json.dumps({"organization_uuid": ALPHA}).encode())

        with patch.object(sessions.urllib.request, "build_opener", return_value=Opener()) as build:
            self.assertEqual(sessions.verify_identity(cookies(), ALPHA)[0]["value"], SECRET)
            self.assertTrue(any(isinstance(item, sessions.NoRedirect) for item in build.call_args.args))

    def test_wrong_identity_or_html_is_not_success(self):
        for body, content_type, expected in ((json.dumps({"organization_uuid": BETA}).encode(), "application/json", "wrong_company"),
                                              (b"<html>login</html>", "text/html", "invalid_response"),
                                              (b"{}", "application/json", "invalid_response")):
            with self.subTest(expected=expected):
                with patch.object(sessions.urllib.request, "build_opener") as build:
                    build.return_value.open.return_value = self.response(body, content_type)
                    with self.assertRaises(sessions.SessionError) as caught:
                        sessions.verify_identity(cookies(), ALPHA)
                    self.assertEqual(caught.exception.code, expected)

    def test_http_errors_are_distinct_and_do_not_print_secrets(self):
        for status, expected in ((401, "expired"), (403, "forbidden"), (302, "redirect"), (500, "invalid_response")):
            with self.subTest(status=status):
                error = urllib.error.HTTPError(sessions.IDENTITY_URL, status, SECRET, {}, io.BytesIO(SECRET.encode()))
                with patch.object(sessions.urllib.request, "build_opener") as build:
                    build.return_value.open.side_effect = error
                    with self.assertRaises(sessions.SessionError) as caught:
                        sessions.verify_identity(cookies(), ALPHA)
                    self.assertEqual(caught.exception.code, expected)
                    self.assertNotIn(SECRET, str(caught.exception))

    def test_network_failure_not_expiry(self):
        with patch.object(sessions.urllib.request, "build_opener") as build:
            build.return_value.open.side_effect = urllib.error.URLError(SECRET)
            with self.assertRaises(sessions.SessionError) as caught:
                sessions.verify_identity(cookies(), ALPHA)
            self.assertEqual(caught.exception.code, "network_error")
            self.assertNotIn(SECRET, str(caught.exception))

    def test_main_never_prints_dependency_exception(self):
        output = io.StringIO()
        with patch.object(sessions, "LocalStore", side_effect=RuntimeError(SECRET)), contextlib.redirect_stdout(output):
            self.assertEqual(sessions.main(["status", "--company-id", ALPHA]), 2)
        self.assertNotIn(SECRET, output.getvalue())

    def test_help_does_not_access_native_vault(self):
        with patch.object(sessions, "LocalStore") as store, contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                sessions.main(["--help"])
        self.assertEqual(caught.exception.code, 0)
        store.assert_not_called()

    def test_native_backend_is_explicit_and_windows_never_roams(self):
        class Backend:
            priority = 5

        windows = types.ModuleType("keyring.backends.Windows")
        windows.WinVaultKeyring = Backend
        mac = types.ModuleType("keyring.backends.macOS")
        mac.Keyring = Backend
        with patch.dict(sys.modules, {"keyring.backends.Windows": windows, "keyring.backends.macOS": mac}):
            with patch.object(sessions.sys, "platform", "win32"):
                self.assertEqual(sessions.native_keyring().persist, "local machine")
            with patch.object(sessions.sys, "platform", "darwin"):
                self.assertIsNone(sessions.native_keyring().keychain)
            with patch.object(sessions.sys, "platform", "linux"):
                with self.assertRaises(sessions.SessionError) as caught:
                    sessions.native_keyring()
                self.assertEqual(caught.exception.code, "unsupported_platform")


@unittest.skipUnless(importlib.util.find_spec("cryptography"), "optional cryptography dependency not installed")
class EncryptedStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.keyring = FakeKeyring()
        self.store = sessions.LocalStore(self.root, self.keyring)

    def test_encrypted_round_trip_metadata_and_permissions(self):
        self.store.save(connected())
        self.assertEqual(self.store.load(ALPHA).cookies[0]["value"], SECRET)
        for file in self.root.rglob("*"):
            if file.is_file():
                self.assertNotIn(SECRET.encode(), file.read_bytes())
                if os.name != "nt":
                    self.assertEqual(file.stat().st_mode & 0o777, 0o600)
        self.assertEqual(len(self.keyring.items), 1)
        key = next(iter(self.keyring.items.values()))
        self.assertLess(len(key.encode("utf-16-le")), 2560)
        self.assertNotIn(SECRET, key)
        metadata = json.loads((self.root / ALPHA / "metadata.json").read_text())
        self.assertNotIn("cookies", metadata)

    def test_ciphertext_swapping_between_tenants_fails_even_with_same_key(self):
        self.store.save(connected())
        self.store.save(connected(BETA, "other-cookie"))
        self.keyring.items[sessions.SERVICE + "." + BETA, BETA] = self.keyring.items[sessions.SERVICE + "." + ALPHA, ALPHA]
        (self.root / BETA / "session.enc").write_bytes((self.root / ALPHA / "session.enc").read_bytes())
        with self.assertRaises(sessions.SessionError) as caught:
            self.store.load(BETA)
        self.assertEqual(caught.exception.code, "storage_error")

    def test_forget_one_tenant_preserves_another(self):
        self.store.save(connected())
        self.store.save(connected(BETA, "other-cookie"))
        self.store.forget(ALPHA)
        self.assertIsNone(self.store.load(ALPHA))
        self.assertEqual(self.store.load(BETA).cookies[0]["value"], "other-cookie")
        self.assertEqual(len(self.keyring.items), 1)

    def test_retention_expired_after_thirty_days(self):
        self.store.save(connected())
        with patch.object(sessions.time, "time", return_value=time.time() + sessions.RETENTION_SECONDS + 1):
            with self.assertRaises(sessions.SessionError) as caught:
                self.store.load(ALPHA)
            self.assertEqual(caught.exception.code, "expired")

    def test_lost_key_never_creates_replacement_for_existing_blob(self):
        self.store.save(connected())
        self.keyring.items.clear()
        with self.assertRaises(sessions.SessionError) as caught:
            self.store.load(ALPHA)
        self.assertEqual(caught.exception.code, "storage_error")
        self.assertEqual(self.keyring.items, {})

    def test_corrupt_blob_or_oversize_rejected(self):
        self.store.save(connected())
        for payload in (b"broken", b"x" * (sessions.MAX_SECRET_BYTES + 65)):
            (self.root / ALPHA / "session.enc").write_bytes(payload)
            with self.assertRaises(sessions.SessionError):
                self.store.load(ALPHA)

    def test_plaintext_keyring_failure_cannot_write_session(self):
        def fail(*_):
            raise RuntimeError(SECRET)

        self.keyring.set_password = fail
        with self.assertRaises(sessions.SessionError):
            self.store.save(connected())
        self.assertFalse((self.root / ALPHA / "session.enc").exists())

    def test_overlapping_operations_same_tenant_fail_but_other_tenant_allowed(self):
        with self.store.transaction(ALPHA):
            with self.assertRaises(sessions.SessionError) as caught:
                with self.store.transaction(ALPHA):
                    self.fail("second operation acquired same-tenant lock")
            self.assertEqual(caught.exception.code, "busy")
            with self.store.transaction(BETA):
                pass
        with self.store.transaction(ALPHA):
            pass

    def test_large_session_uses_small_keyring_record(self):
        self.store.save(connected(value="s" * 8000))
        self.assertEqual(len(self.store.load(ALPHA).cookies[0]["value"]), 8000)
        self.assertTrue(all(len(value.encode("utf-16-le")) < 2560 for value in self.keyring.items.values()))

    def test_corrupt_store_blocks_login_and_preserves_other_tenant(self):
        self.store.save(connected())
        self.store.save(connected(BETA, "other-cookie"))
        (self.root / ALPHA / "session.enc").write_bytes(b"broken")
        with patch.object(sessions, "interactive_login") as login:
            manager = sessions.SessionManager(self.store, lambda jar, _: jar, login)
            with self.assertRaises(sessions.SessionError) as caught:
                manager.connect(ALPHA)
            self.assertEqual(caught.exception.code, "storage_error")
            login.assert_not_called()
        self.assertEqual(self.store.load(BETA).cookies[0]["value"], "other-cookie")

    def test_status_refresh_does_not_extend_absolute_retention(self):
        initial = connected()
        initial.created_at -= sessions.RETENTION_SECONDS - 100
        self.store.save(initial)
        manager = sessions.SessionManager(self.store, lambda jar, _: jar)
        refreshed = manager.status(ALPHA)
        self.assertEqual(refreshed.created_at, initial.created_at)
        with patch.object(sessions.time, "time", return_value=time.time() + 101):
            with self.assertRaises(sessions.SessionError) as caught:
                manager.status(ALPHA)
            self.assertEqual(caught.exception.code, "expired")

    def test_forget_can_remove_corrupted_key(self):
        self.store.save(connected())
        self.keyring.items[sessions.SERVICE + "." + ALPHA, ALPHA] = "invalid-base64-key"
        self.store.forget(ALPHA)
        self.assertEqual(self.keyring.items, {})
        self.assertIsNone(self.store.load(ALPHA))


if __name__ == "__main__":
    unittest.main()

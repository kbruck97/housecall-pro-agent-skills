# Optional local connection runtime

This helper is a new bounded implementation. Synthetic tests validate its logic; native Windows/macOS vault and interactive HCP login must be tested independently. A previous developer's connection is not proof this user's installation works. It provides status/connect/forget and fixed identity GET only, not general internal API operations.

## Agent setup

Read the project's and runtime's policies before launching a browser. Use the calling agent's permitted browser tooling; do not substitute this helper where tool policy forbids it. If the runtime cannot securely transfer an authorized browser session, explain the exact capability gap.

Install Python 3.10+ and the optional dependencies in an isolated environment. Choose a user-owned runtime folder outside the repository/installed skill, then create the environment there, replacing `python` with the discovered Python 3 executable (`py -3` may be appropriate on Windows):

```sh
python -m venv <local-runtime-folder>/.venv
```

On Windows, use `<local-runtime-folder>\.venv\Scripts\python.exe`; on macOS, use `<local-runtime-folder>/.venv/bin/python`. For the next commands, set the working directory to the skill folder. Use that executable for each of these commands:

```sh
python -m pip install -r requirements.txt
python -m playwright install chromium
python scripts/local_sessions.py --help
python scripts/local_sessions.py status --company-id <trusted-company-uuid>
python scripts/local_sessions.py connect --company-id <trusted-company-uuid>
```

The examples' `python` means the selected virtual environment executable, not a request to replace the system Python. Install only from official package registries/vendor browser distribution. Dependencies belong in the environment, never in the distributed skill archive. A fresh browser download needs internet access. `connect --timeout 300` gives the user a bounded login period; use the documented bounds rather than an indefinite unattended browser.

## Session storage

The agent must resolve the expected internal `organization_uuid` from a trusted mapping. Public company records can help establish this mapping, but do not pass an arbitrary company/location `id` without verifying that it is the same internal UUID.

The helper creates an independent per-company encryption key in the native OS vault. The encrypted cookies and safe metadata are in:

- Windows: `%LOCALAPPDATA%\TSM\HousecallPro\<company-uuid>\`
- macOS: `~/Library/Application Support/TSM/HousecallPro/<company-uuid>/`

The files are `session.enc` and `metadata.json`; the vault service is `TSM.HousecallPro.local-session.v1.<company-uuid>`, account `<company-uuid>`. Windows vault persistence is local machine. Native OS backends are required; fallback/plaintext backends and unsupported OSes are refused. A locked vault may require the user to unlock or allow access through the OS. Never create a plaintext fallback. Do not move the saved connections into the repository or shared/cloud-synced folders.

The helper stores only approved HCP-scoped session/CSRF cookies after identity verification. It does not save passwords, MFA codes, arbitrary browser local storage or full browsing profiles. It never reads the ordinary Chrome cookie database. The maximum reuse age is 30 days from login; HCP may revoke or expire a session sooner. Expired encrypted material remains until successful reconnect or explicit forget; it is not automatically purged. A harmless `.connection.lock` file may remain after forget to prevent races between processes.

## Passing a connection to another adapter

The CLI reports nonsecret identity/status only. A reviewed adapter may import the helper in the same process; do not use CLI output to transfer credentials. With this skill's `scripts` directory on the adapter's Python import path:

```python
from local_sessions import LocalStore, SessionError, SessionManager

store = LocalStore()
manager = SessionManager(store)
try:
    connection = manager.status(expected_company_uuid)
except SessionError as error:
    # error.code is a fixed safe status; never print upstream exceptions.
    handle_connection_status(error.code)
else:
    # Only an independently reviewed operation adapter may consume this object.
    # Never print, JSON-serialize, log, or return connection.cookies to the model.
    reviewed_adapter.perform_authorized_operation(connection)
```

`expected_company_uuid`, `handle_connection_status` and `reviewed_adapter` are application-supplied, not bundled functions. `VerifiedSession` contains `company_id`, in-memory `cookies`, original `created_at`, and current `verified_at`; its repr excludes credentials. `status()` verifies the identity now and saves rotated cookies returned by that identity GET, preserving original creation time and the absolute reuse-age limit. The connection is not a permanent identity guarantee.

The operation adapter must enforce an independently reviewed exact host/method/path/schema and a fresh company check before the action. Do not call `LocalStore.save()` on unverified browser or operation data. If an operation rotates cookies, the adapter must validate the new jar through `verify_identity(new_cookies, expected_company_uuid)` before storing a replacement `VerifiedSession`, preserve `created_at`, and serialize the complete read/operation/verification/save sequence through `store.transaction(expected_company_uuid)` to prevent another process overwriting a newer session. These business-operation lifecycle details are not implemented by the connection CLI; do not claim it already supports an event/job mutation.

`connect()` is the interactive variant: it reuses a valid saved session and only prompts when `status` resolves to `missing` or `expired`. Do not hold an outer `store.transaction` while calling `status()` or `connect()`, because those methods already acquire it. Inside an adapter-owned transaction, use the documented lower-level load → `verify_identity` → authorized operation → `verify_identity` → save sequence rather than nesting the manager's lock.

Safe error routing:

- `missing` / `expired`: explain login need; run one `connect` if authorized.
- `wrong_company` / `forbidden`: stop the action; resolve the company mapping or access without account hopping.
- `network_error` / `redirect` / `invalid_response`: retain the session, diagnose connectivity or contract drift; do not assume logout.
- `storage_error` / `unsupported_platform` / `dependencies_missing`: resolve the local capability; no plaintext fallback.
- `login_cancelled` / `login_timeout` / `browser_error`: report incomplete login; do not claim connection or loop automatically.
- `busy`: another operation holds this tenant's lock; retry after it finishes.
- `invalid_cookie` / `invalid_company` / `unsafe_debug`: correct the input/runtime contract without displaying secrets.

There is no arbitrary `--url` request option. Authentication success does not establish a business route, its CSRF requirements, notification behavior or write authorization.

## First-run acceptance

On the intended Windows/Mac machine, separately verify: official login and MFA, exact company match, encrypted storage/native vault access, browser cancellation, process restart and session reuse, second-tenant isolation, expired-session recovery, and removal of one local connection. Use a read-only identity check first. Do not perform mutations solely to test connectivity. Record which platform/version and steps were actually tested; leave untested steps explicit.

## Technical sources

- [Playwright browser contexts](https://playwright.dev/python/docs/api/class-browsercontext): nonpersistent contexts and in-memory authentication state.
- [Playwright API testing](https://playwright.dev/python/docs/api-testing): request contexts can share a browser context's cookies.
- [Playwright request options](https://playwright.dev/python/docs/api/class-apirequestcontext): redirect and timeout controls.
- [Windows credential storage limits](https://learn.microsoft.com/en-us/windows/win32/api/wincred/ns-wincred-credentialw): a credential blob is size-limited, so only the encryption key goes in the vault.
- [keyring native Windows backend](https://github.com/jaraco/keyring/blob/main/keyring/backends/Windows.py): persistence selection.

The `/alpha/pro` identity endpoint and session/CSRF names are observed internal HCP behavior, not an official public contract. A changed schema must stop the helper, not be guessed around.

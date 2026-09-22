---
name: hcp-connections
description: Connect Housecall Pro locally, reuse separate company sessions, guide interactive sign-in and MFA, and recover expired sessions without putting credentials in chat.
license: MIT
version: 1.0.0
---

# Local Housecall Pro connections

Use for “connect this company,” first login, missing/expired sessions, switching among companies, verifying a saved connection, or forgetting a local connection. Read the [session workflow](references/internal-session-workflow.md) for company isolation, error handling and storage. This optional helper handles login and identity only; it is not a business-operation SDK. Windows and macOS native login/vault behavior must be verified on the user's computer before claiming that computer is connected.

## Choose the connection

Use the public API when sufficient. Retrieve the intended company's existing API key from the user's configured secret provider, such as 1Password, through that provider's supported tools. Keys use `Authorization: Token` at `api.housecallpro.com`; a website login is separate. Do not ask for cookies simply because the public API key is absent, or switch surfaces after access denial.

For an authorized internal-session task, resolve the expected company UUID from trusted configuration or a verified mapping from public `GET /company` identity to internal `organization_uuid`. Keep company UUIDs literal; do not assume a generic public `id`, numeric organization ID or location ID is interchangeable with the internal UUID. Never bind the requested company name to an unverified currently signed-in company. If no trusted identity mapping exists, obtain that mapping before running this helper.

## Execute locally

1. Discover the host OS and available tools. Local execution, HTTPS, an allowed Playwright browser controller, and native credential storage are required. A chat-only runtime cannot execute these instructions. The helper has no VPS dependency. Honor the user's browser constraints: if interactive login is needed but browser use is prohibited, explain that specific dependency instead of launching it.
2. Prepare the optional runtime using [setup](references/setup.md). Run the commands for the user when permitted; do not hand a nontechnical user a terminal/key-copy exercise. Use an existing compatible runtime or an isolated virtual environment. Do not overwrite installed skills or credentials.
3. Run `python scripts/local_sessions.py status --company-id <expected-uuid>` from this skill folder, using the selected environment's Python. `status` performs a live identity check; it does not open a login window or print cookies. A successful local file check is not sufficient.
4. If missing or authentication is required, tell the user: “I need you to sign in to Housecall Pro for [company] in a local window and complete any verification there. I will verify the company and save its connection on this computer.” Run `python scripts/local_sessions.py connect --company-id <expected-uuid>`. It rechecks reuse first, then opens a dedicated login window only when needed. Let the user enter password/MFA on HCP's official page. Never ask for passwords, cookies or MFA codes in chat. The dedicated browser may not include their usual password-manager extension.
5. Keep the helper running while the user logs in. Read the bounded nonsecret result. Only matching live company identity allows the helper to save the HCP session/CSRF cookies, encrypted locally with the key in the OS vault. A cancelled or failed login is not connected; report its specific result. Do not resubmit the original business action if it might already have succeeded.
6. Reuse the verified company connection for a separately reviewed operation adapter. There is intentionally no arbitrary URL, raw cookie export, or business-write CLI. Follow the helper's documented in-process interface and the domain skill; login success does not establish CSRF/write readiness or authorization for another action.
7. On a later request, start with that company's `status` again. Only missing/expired/unauthenticated state calls for login. Forbidden access, wrong company, network failure, schema drift or unavailable/locked native vault must be handled as their own errors; do not erase sessions or automatically loop through accounts.
8. On an explicit request to remove a saved connection, run `python scripts/local_sessions.py forget --company-id <expected-uuid>`. This removes only local saved connection material, not HCP server-side sessions or another computer's connection.

## What to report

Report the verified company, whether the connection was reused or newly established, where the local encrypted record lives, and any unresolved prerequisite. Keep installed, connected, read-tested and write-tested distinct. Do not display secrets, full headers, raw browser state, login screenshots, provider traces or arbitrary exception text.

## Repeatable behavior

When companies A–E have been connected, a later B request must load B's stored record and verify B. It must not use the last active company E. A missing or expired B session requires a B login; the other four sessions remain intact. Saved sessions are local to the user/computer, independent of the shared 1Password API-key environment.

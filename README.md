# Housecall Pro agent skills

**MIT licensed.** This is a modular operational skill pack with executable offline validation/packaging helpers and an optional local connection helper, **not a general HCP SDK or an installed live integration**. No credentials, customer case corpus, profile configuration or private path/hash inventory is distributed. The included RivetFlo-owned material is released with explicit owner authorization under [MIT](LICENSE); historical attribution is preserved in [NOTICE](NOTICE.md). Housecall Pro has not endorsed this independent project.

## Use

Start with `hcp-operations`, then `hcp-foundations` and the appropriate domain skill. Each folder under `skills/` is a self-contained package: read its `SKILL.md`, follow linked references, and preserve its frontmatter. Equipment work has seven dedicated source-family modules; customer journeys remain separate from source/data operations. See [document index](DOCUMENT_INDEX.md) for every package and reference.

The [capability ledger](docs/capabilities.json) labels official-public, observed-internal, UI-only and unverified operations. Official-public means documentation evidence—not entitlement, implemented transport, complete payload schema or authorization. Sidebar/changelog-only entries need endpoint-body/schema confirmation before use. Verification dates are **2026-09-21 discovery-snapshot attribution**, not independent per-URL fetch timestamps or tenant probes.

## API-first access

Use the supported public API when sufficient. For UI-backed work otherwise, prefer a verified authorized Alpha/internal-session API over UI clicking. Browser use remains appropriate for secure login/MFA/session bootstrap, visual verification and unavailable routes. Follow the [internal-session workflow](docs/internal-session-workflow.md); it requires runtime secure-session/HTTP capability and current tenant, CSRF/header/schema and operation verification. For local interactive sign-in and separate saved company sessions, use [hcp-connections](skills/hcp-connections/SKILL.md). Its optional helper verifies identity and stores encrypted sessions locally; it does not provide business operations or a permission bypass. Native Windows/macOS login and vault behavior still require first-run verification.

## Prerequisites and setup

- Offline tools: Python 3.10+ standard library; base tests exercised with Python 3.12; the local-connection update passed the full synthetic suite on macOS with Python 3.14. No pip packages or network needed for distribution/contract checks. To run all optional connection encryption tests without skips, install the connection skill's requirements in an isolated test environment.
- Agent consumption: a Hermes-compatible skill loader, or an agent that reads SKILL.md directly. No automatic production installation.
- Optional connection runtime: [setup](skills/hcp-connections/references/setup.md) uses Python, Playwright/Chromium, keyring and cryptography. Session encryption keys stay in the native OS vault; encrypted company sessions stay on that computer. No VPS or shared cookie environment is needed.
- Business-operation runtime: supply your own tenant-isolated public API, private-web, FI, communications and scheduling adapters under the [adapter contract](docs/adapters.md). Keys/sessions/OTP stay in the deployment's secret provider. No private auth/session helper from source profiles is bundled.
- Public auth: read-only key preferred, `Token` scheme; partner OAuth uses `Bearer`. Confirm MAX/XL entitlement conflict with the tenant administrator.

Run from repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

On a shared production host follow its fleet lock, nice/load policy before tests; the generic commands above do not acquire site-specific locks. Tests use synthetic inputs, fake vault/HTTP/browser dependencies and fresh temporary snapshots only. They validate contract helpers—not actual APIs, live OCR, equipment adapters, consent language classification or a complete sender.

## Local sessions across companies

The agent checks the requested company's saved session before asking for login. Missing/expired sessions trigger an interactive official HCP sign-in; passwords and MFA stay on that page. After exact company verification, each session is stored separately. Returning to company B after connecting A–E loads B's record and verifies B again. API keys in 1Password remain separate; they do not create website cookies. See [the connection skill](skills/hcp-connections/SKILL.md) for execution and storage paths.

## Build and stage locally

Choose an explicit fresh directory; do not target an installed profile:

```sh
scratch=$(mktemp -d)
python3 scripts/package.py build --output "$scratch/hcp-skills.tar"
python3 scripts/package.py stage --archive "$scratch/hcp-skills.tar" --destination "$scratch/staged"
python3 scripts/validate.py "$scratch/staged"
```

The root [maintenance adapter](AGENTS.md) is required in both the source and staged distribution and is covered by the package manifest. The uncompressed tar is deterministic (sorted paths, normalized metadata); its receipt prints SHA-256. Stage verifies every archive member and digest, validates the extracted pack and refuses existing destinations, symlinks, traversal, unexpected roots, duplicate members and excessive size. Local attacker races in writable parent directories are outside the threat model: use an operator-owned private scratch directory. A manifest hash detects accidental corruption, **not source authenticity**; receive the archive SHA through a trusted channel.

Staging is not installing. To test one skill, read its staged `skills/<name>/SKILL.md` and its own references; public modules carry self-contained copies of the capability ledger and adapter reference. Install only after explicit approval into a selected test profile by the supported Hermes method. Keep credentials/tenant overlays external. Rollback is removing only the newly created approved staging directory, never deleting source/profile data.

## Coverage and boundaries

- Customers/addresses; jobs/history/attachments; schedule/reschedule/cancel boundary/dispatch; estimates/options; invoices/payment allocations; pricebook/internal templates/BOM; leads/pipeline; employee/config reference; reporting completeness; webhooks/security/recovery.
- Seven equipment families preserve collection, installed-new versus serviced-existing, physical-unit evidence, nameplates, reconciliation and HVAC lookup.
- CSR routing/customer service, lead/estimate/invoice follow-up, happy calls, scanner, scheduling and completed-job marketing retain tenant-parameterized policy and durable receipt/consent gates.
- [Source disposition](docs/source-disposition.json) accounts for all 38 inventoried families, 123 instances and 61 package variants using sanitized opaque labels; private resolver remains outside the pack. Exclusions identify unrelated or obsolete operational material, not silently dropped HCP capabilities.
- [Migration decisions](docs/MIGRATION.md) records conflict resolution and adapter gaps. [Offline contracts](docs/OFFLINE_CONTRACTS.md) explains helper limits and test evidence.

## Remaining gaps / no claims

The new connection helper has synthetic coverage; native Windows/macOS login, real OS-vault storage and HCP session reuse have not been exercised by this release. No live entitlement, OCR engine, provider sender, FI store or write adapter was exercised. No public equipment/charge/refund/invoice-send/service-plan CRUD is established. Checklist schemas, standalone appointments, employee writes and generic audit/report APIs remain unverified. No CI-hosted run, production installation, deployment or tenant validation is implied. Historical source inventory drift is documented, not represented as a frozen-corpus audit. The root [maintenance adapter](AGENTS.md) is included in validation and packages. See [distribution policy](docs/DISTRIBUTION.md) for the public export boundary. Automated privacy patterns are a safety net, not proof against all PII; review the complete distribution before sharing.

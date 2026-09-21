# Editorial provenance and portability decisions

Base: the single inventoried hcp-alpha-data-collection source variant, read in full. Selected reusable references read: alpha-collection-envelope-normalization.md, public-alpha-parity-parser-contract.md, full-equipment-audit-pagination-parity.md, and equipment-transaction-full-history-job-discovery.md. Source filenames here are provenance prose, not dependency links; no historical case files are bundled.

Retained: nested-list normalization, public `jobs` envelope handling, exact-customer gating, per-job detail after full discovery, unique-ID pagination proof, source union/parity, equipment-by-property isolation, media classification, and explicit unknown states.

Changed for portability and safety:

- Public evidence gathering remains usable, but missing private equipment cannot be replaced by public job reads. This resolves the source's broad “never fall back” wording without erasing its duplicate-prevention purpose.
- The source session helper and private MFA integration were outside the package or environment-specific. They are not included or advertised as installed tools; authentication is an adapter responsibility.
- Private alpha/React paths, response contracts, and historical filter/sort behavior are observations requiring explicit opt-in and validation, not a supported universal public API.
- Replaced raw JSON persistence with a minimized allowlist and private runtime index. Removed all account details, local paths, hostnames, signed URLs, real IDs, and credential handling recipes.
- Broader tenant scans and alternate-order pagination are conditional on authority and adapter support. Equal unique totals do not establish a transactional snapshot.
- Removed automatic attach/write steps from collection. No cleanup/probe writes are allowed.
- Replaced case chronology and case filenames with synthetic test classes. No external source scripts, backups, or historical data are copied.

The source inventory report and manifest were used privately to choose the single variant and identify missing dependencies; they are not redistribution artifacts. This owner-authorized MIT distribution does not establish runtime capability or current endpoint behavior. Complete packaging verification is offline editorial validation only.

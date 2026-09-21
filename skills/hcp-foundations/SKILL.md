---
name: hcp-foundations
description: Use when selecting HCP access and validating API scope. Establish authentication, capability, pagination, and safety gates.
license: MIT
version: 1.0.0
---

# HCP foundations

## Scope and evidence

Use this before any Housecall Pro collector or write workflow. This package describes capabilities; it does not install an API client or confer permission to act. The documentation research snapshot is associated with 2026-09-21; this is not live tenant verification. Consult the [capability ledger](references/capabilities.json) for official source URLs and evidence limits, and the [adapter contract](references/adapters.md) before implementation.

Keep four questions separate: is the operation documented, is the tenant entitled, does the adapter implement it, and did the user authorize this action? All four must pass for writes. A documented endpoint is not a successful integration test.

## Select a surface

| Surface | Appropriate use | Boundary |
|---|---|---|
| Official public API | Documented CRM, catalog, financial reads and explicitly listed writes | API origin `api.housecallpro.com`; exact operation/security schema required |
| Observed internal web API | Missing property/equipment or billing-parent evidence through an independently authorized adapter | `/alpha` observations are tenant-specific, not the public contract; no silent fallback |
| UI-only/manual | Admin setup and unsupported operations after owner approval | A UI button does not establish an API endpoint |
| Field Intelligence (FI) or another integration | Derived evidence, local job state, processing/recovery ledgers | Not HCP; provenance, freshness, authorization, and tenant isolation must be explicit |

A hybrid key that once accessed an internal path does not make that path officially public. Partner Jobs is separately onboarded and is not the normal Pro API for accounting, workflow, marketing, or subcontractor tools.

## Authentication and company scope

1. Resolve the exact tenant/company from trusted configuration, not model-generated names or incoming free text. Refuse conflicting company selectors.
2. Prefer an Admin-issued **Read-only** API key for discovery. Official Help documents Full access and Read-only keys; only Admin users generate/delete them.
3. Use `Authorization: Token <API_KEY>` for API keys and `Authorization: Bearer <OAUTH_ACCESS_TOKEN>` for partner OAuth. Never substitute one scheme for the other. Retrieve credentials through the deployment's secret provider, never chat or exported files.
4. OAuth authorization-code integration is reserved for official partners. Read expiry from the grant; do not hardcode example expiry or invent granular scopes. The researched example scope is `public`, not a universal scope catalog.
5. Pin `X-Company-Id` when supported by the selected operation. It overrides legacy `location_ids`; do not send conflicting values. Multi-location keys reach the owner and descendants, not ancestors or unrelated locations. OAuth can be narrower based on accessible organizations.
6. Preserve the plan conflict: developer home says MAX or XL; Help says MAX only. Verify current tenant entitlement with its administrator/HCP rather than choosing a convenient interpretation.
7. Pricebook overview requires an organization-specific API key; do not infer universal OAuth access.

Never expose tokens, cookies, signing secrets, credentialed URLs, or full request headers. Use separate credential contexts per surface and tenant.

## Complete, bounded collection

- Configure pagination per endpoint. Customers, employees, jobs, estimates, invoices, and events use `page`/`page_size`; **routes use request `per_page` but response `page_size`**. The research did not establish a universal maximum page size.
- Read list metadata (`page`, `page_size`, `total_pages`, `total_items`), fetch every required page, deduplicate by canonical resource identity, and verify row company/customer scope. A successful response does not prove its filter worked.
- Stop on repeated pages, malformed envelopes, changing totals that prevent reconciliation, or a configured time/page budget. Return `partial` with the checkpoint and remaining gap; never label a budget-truncated scan complete.
- Keep attempt-level errors separate from final endpoint coverage. A recovered 429 is not a permanent gap. Unexpanded fields are unknown, not absent.
- Use stable sort where documented; for changing datasets report the scan interval and reconcile overlapping boundaries. Pagination alone does not provide snapshot isolation.

## Errors and mutations

On 401/403 stop and diagnose scheme, key permission, entitlement, company scope, and origin; never turn failure into an empty dataset. On 404 check canonical identifier and operation evidence before concluding the resource does not exist. On validation failure repair only against the exact schema, not invented parameters.

A 429 may include epoch `RateLimit-Reset`. Convert from epoch time, wait until reset plus jitter, and use a bounded retry/time budget. No numeric universal rate ceiling was verified; do not embed folklore limits. Missing or invalid reset headers use a bounded backoff policy, not an unbounded tight loop.

Before an authorized mutation: re-read target, validate company/address, capture explicit field-level intent and notification effects, and record a local intent. Submit once, save the receipt, then read the exact target back. A timeout after submission is `ambiguous`; reconcile before retry. Local dedupe is not a documented server idempotency guarantee. Deletions, bulk replacements, locks, customer notifications, scheduling, financial actions, and publication require separate approval scope. No live create/delete probes.

## Examples and completion

**Positive:** A read-only customer export uses a company-pinned Token credential, collects every documented page, checks returned scope, and reports the final coverage with no sends.

**Negative:** A 401 is treated as “no customers,” then the collector tries private equipment POSTs with the same key. Stop instead; neither fallback access nor writes were authorized.

Done means the chosen surface, auth scheme, company scope, operation evidence, paging completion, and gaps are recorded without secrets. If required schema evidence or authority is missing, return `blocked` with the precise missing prerequisite.

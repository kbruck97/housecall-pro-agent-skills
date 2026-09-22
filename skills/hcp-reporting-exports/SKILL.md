---
name: hcp-reporting-exports
description: Use when deriving HCP reports or exports. Reconcile scoped resources, financial allocations, freshness, and privacy without sending data.
license: MIT
version: 1.2.0
---

# HCP reporting and exports

Use foundations (dependency skill `hcp-foundations`) and [adapter contracts](references/adapters.md). Reports are derived from documented reads and authorized integration ledgers; no general public reports/dashboard/export/audit-log endpoint was established. Source coverage and limits are in the [capability ledger](references/capabilities.json).

## Define the report before collection

Record tenant/company, cohort, interval and timezone, metric definitions, recipient/purpose, allowed fields, and inclusion/exclusion rules. Define whether “recent” means created, scheduled, completed, paid, or updated time. Select the actual supporting resource rather than relabeling a convenient field. Calendar events are not audit events. API reads during an interval are not an atomic snapshot.

Use separate states for `documented`, `collected-complete`, `collected-partial`, `failed`, `not-requested`, and `unavailable`. Failed reads cannot become zero-valued metrics. FI/local cache data must retain source surface, collection/processing timestamps, and freshness warnings; it cannot silently replace current HCP truth.

## Collection and financial reconciliation

1. Page all required documented resources, preserving per-endpoint metadata, IDs, returned scope checks, and scan start/end. Bound cost safely; when a bound stops collection, return partial rather than a fabricated denominator.
2. Invoice list uses `customer_uuid` **array** and page/page_size. Use schema-approved array encoding; do not substitute customer_id or a guessed job_id filter. Resolve invoice job relationships to validate company/customer scope.
3. Keep invoice status, `due_amount`, dates, payment records and job balance separately. Query filters are `amount_due_min`/`amount_due_max`, while response balance is `due_amount`; do not silently rename API parameters. Null due/paid dates are unknown, not zero/epoch dates.
4. For split/progress invoices, aggregate allocated line-item **`invoiced_amount`**, not repeated original `amount`. Null allocation stays unknown and prevents a complete allocated-total claim. Deduplicate invoice identities, not shared line descriptions. Document currency/unit semantics from the relevant schema before conversion, and reconcile taxes/discounts separately.
5. Deduplicate jobs independently of invoices. A paid deposit/progress invoice does not mean the job is paid in full. Happy-call candidate reports require current completed job state, final invoice/payment reconciliation, and zero outstanding job balance; conflicting timestamps/statuses or missing finality evidence hold review. This is eligibility reporting, not permission to contact anyone.
6. Estimate conversion reports must distinguish parent and option states. `approval_status_updated_at` is last status change, not approved-at; a later decline or cleared status defeats the assumed approval timestamp. Preserve unknown approval time rather than inventing a sale date.
7. Compare current HCP records with any authorized local projection by exact identity and freshness, yielding missing, stale, conflicting, and unresolved rows. Do not run workers or write local tables just to inspect reconciliation.

## Export safely

Build a strict allowlisted projection. Remove names/contact/address/access instructions and free-text content unless indispensable and expressly authorized for a restricted recipient. Filenames, descriptions, image metadata, and structured names may contain PII. Never export cookies, tokens, signed URLs, raw webhook payloads, or private tenant policies into a reusable package.

Keep raw evidence private and access-controlled, with retention and deletion policy; distributable artifacts use synthetic placeholders or privacy-reviewed aggregates. Escape CSV formula-leading cells, neutralize active HTML, and handle exported text as untrusted content. Maintain provenance in private references rather than publishing resolvable customer IDs. Sending, uploading, dashboard publication, and customer messages require separate approval.

## Report shape and acceptance

Return: as-of interval; source/metric definitions; complete/partial coverage; counts and distinct denominators; findings; excluded/unknown rows; reconciliation differences; privacy checks; next action. Verify totals programmatically, every claimed join, status mapping, empty-versus-unexpanded distinction, and sanitized artifact content before delivery.

**Positive:** A split-invoice report excludes unknown allocations from the known subtotal and reports an incomplete allocation count rather than treating null as zero.

**Negative:** A page of paid invoices is called “all completed jobs,” exported with signed image links, then sent to marketing. Reject all three: incomplete coverage, false lifecycle equivalence, and unauthorized disclosure.

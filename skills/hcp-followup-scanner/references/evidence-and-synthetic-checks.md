# Scan evidence contract and offline acceptance cases

## Report shape

This is an internal reporting schema, not a promised provider response. Example is wholly synthetic; counts describe only the three invented rows below.

```yaml
schema_version: 1
intent_label: scanner_request
mode: read_only
tenant_ref: synthetic-tenant
as_of: null # operational run must supply real timestamp and timezone
source_kind: supplied_fixture
adapter_binding: null
mapping_version: synthetic-map-v1
completeness: complete_for_fixture
pagination: {pages: 1, exhausted: true, truncated: false}
counts:
  scanned: 3
  due: 2
  eligible_dry_run: 0
  blocked_due: 1
  unknown_due: 1
  not_due: 1
rows:
  - item_ref: synthetic-invoice
    workflow: invoice
    due: true
    classification: blocked
    reasons: [source_settled_queue_stale]
    evidence_refs: [synthetic-invoice-read, synthetic-job-read]
  - item_ref: synthetic-happy-call
    workflow: happy_call
    due: true
    classification: unknown
    reasons: [consent_source_unavailable]
    evidence_refs: [synthetic-queue-read]
  - item_ref: synthetic-estimate
    workflow: estimate
    due: false
    classification: not_due
    reasons: []
    evidence_refs: [synthetic-queue-read]
disabled_workflows: [appointment_reminder]
mutations_performed: []
next_safe_action: review_stale_invoice_and_restore_read_only_consent_visibility
```

Operational records add actual source binding (redacted in shared reports), source observation/through-date, cutoff/timezone, filter definition, snapshot identity, schema version, freshness verdict, stable item/job/invoice/estimate linkage, raw status/outcome and derived stage, policy/consent/ownership receipts, send/task receipts, due timestamp and next-safe-action.

Define the counted population before totals. For known due state, partition due items into eligible, blocked and unknown-decision buckets; count multiple block reasons separately, not as extra items. If due itself is unknown, use a separate `unknown_due_state` bucket outside the due denominator. Partition all scanned rows into due, not-due and unknown-due-state. Workflow totals must use the same scope and deduplicated key. Owner-disabled workflows may not have been enumerated: distinguish `not_scanned_disabled` from a verified zero. Mark errors and samples as partial; never extrapolate.

## Failure and evidence rules

- 401/403 or missing authorization: stop that source, no credential guessing.
- Rate/timeout errors: bounded authorized read retries only; report partial data if unresolved.
- Same display number matches multiple records: ambiguous, no guessed linkage.
- Export older than policy: historical assessment only, not present eligibility.
- Conflicting paid status and job balance: explicit conflict, no closure or send.
- Runtime gates off: eligible in dry-run if otherwise supported, never sent.
- Promised office action without a durable task: flag unfulfilled/unconfirmed handoff, not proof a human owns it.
- Provider accepted but delivery unknown: do not count as delivered; no automatic resend.
- Wrong tenant in any record: quarantine that evidence, stop affected conclusions and report isolation failure.

## Synthetic checks for an implementation

| Case | Expected audit result |
|---|---|
| Pagination returns one limited page and a next cursor | Partial until exhausted; no global count |
| Existing SQLite path missing | Read-only open fails; no empty database created |
| Raw labels map to awaiting office after review delivery | Display mismatch; no new outreach |
| Customer says paid, invoice still open | Payment claimed/verify source; stop collection cadence for human review |
| Paid invoice but positive linked job balance | Not fully settled; conflict/remaining balance |
| Professional-approved estimate, no conversion | Review bucket, not customer won |
| Option-linked converted job | Confirm conversion only with exact tenant/link evidence |
| Another lane receives STOP | All proactive eligibility blocked |
| Reminder producer disabled, stale item supplied to fake runner | Zero provider calls; ownership reason |
| On-the-way same event twice | One fake send; replay idempotent |
| Source appointment canceled before replay | Zero obsolete on-the-way sends |
| Dual-purpose unit plus duplicate component row | No false two-unit audience qualification |
| Handoff write returned error, board says awaiting office | Unconfirmed task, not accepted work |
| Missing webhook ledger | Unknown coverage, not zero webhook activity |

Do not claim these contract cases passed against a real system unless actual test output is attached. This package's offline documentation validation is separate from runtime acceptance.

## Variant reconciliation

Three scanner mains contributed distinct useful rules: common source-resolution/read-only/reconciliation behavior; newer reminder-owner and final-runner checks; and a separate happy-call delivered-versus-display audit. All five unique reusable scanner references contributed. Tenant-specific paths, board IDs, database names, private event examples, timing constants and live incident findings were removed. Repair/shutdown operations are described only as separately approved implementation requirements, never scan side effects.

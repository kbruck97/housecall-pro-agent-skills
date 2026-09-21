# Plan and receipt contracts

These are portable editorial contracts, not provider request schemas. An integration must map them to its actual validated runtime. Runtime identifiers and raw evidence remain in a restricted mapping outside shared artifacts. Examples use invented aliases that must never be sent to an API.

## Input envelope

| Field | Type / allowed values | Validation |
|---|---|---|
| schema_version | string | Explicitly version the contract. |
| scope | object | tenant_alias, customer_alias, property_alias required; all source rows prove this relationship. |
| modes | array | installed-new and/or serviced-existing; classify each unit independently. |
| stores | array | hcp required; field-intelligence optional and explicitly enabled. |
| coverage | array of objects | collection, status (complete/partial/failed/not-authorized), pages_seen, next_page_present, scope_checked, evidence_cutoff. Complete requires exhausted pagination and verified row scope. |
| evidence | array | alias, kind, locator, unit_subject, observed_fact, supports, contradicts, limitations. Locator is a sanitized page/table/line marker, not a raw filename or signed link. |
| address_bindings | object | Separate typed HCP-property and FI-property aliases; mapping evidence required for both-store mode. |
| authorization | object | read_scope, allowed_operations, approval_reference, expiry or freshness condition; no credential values. |

A missing collection must not become an empty array without a coverage flag. An empty complete list and a failed list have different meanings. Nullable identity fields mean not established; do not persist the text UNKNOWN as a model or serial.

## Physical-unit plan

| Field | Type / rule |
|---|---|
| unit_alias | Unique stable alias within this plan; independent of record count. |
| mode | installed-new or serviced-existing. |
| job_relation | installed / serviced / unrelated / unresolved. |
| existence_basis | Evidence aliases plus explicit quantity and rationale; no quantity from repeated invoice states. |
| identity_status | established / disputed / insufficient. |
| claims | Array of {store, record_alias, disposition}; a record appears at most once across units. |
| fields | Map of field to {current, proposed, evidence, status}; status supported/unknown/conflicting. |
| untouched_reason | Required for unchanged existing units. |
| actions | Ordered operation aliases; no hidden merge or implicit destructive cleanup. |
| unresolved | Array of {field_or_invariant, candidates, reason, evidence_needed}. |

Allowed dispositions: keep, enrich, create-counterpart, link, merge-duplicate, retire, leave-unresolved. A proposed merge must identify survivor, losing representation, evidence of sameness, association transfer, and history preservation. If the adapter cannot preserve required history, hold the merge. Do not silently map retirement to hard deletion.

## Operation ledger

Each operation records: operation_alias; unit_alias; target_store; target_record_alias (null only before create); verb; desired_fields; preconditions; evidence_aliases; approval_reference; dependency_operations; idempotency_key; attempt_state; response_class; written_record_alias; readback_state; field_comparison; association_comparison; unresolved.

- `attempt_state`: planned, refused, transport-unknown, accepted, readback-verified, or readback-mismatch.
- `preconditions`: expected version when available, expected identity fields, property binding, and existing linkage. Re-read and compare if version guards are unavailable; disclose residual concurrency risk.
- `field_comparison`: one row per requested field with requested, observed, and equal boolean. Equality must respect provider null/date normalization without silently changing identity text.
- `idempotency_key`: stable per approved logical operation, never regenerated merely because transport timed out. Do not assume the provider supports native idempotency; verify capabilities and reconcile state before retry.
- Distinguish accepted writes from verified postconditions. A successful response may count in a writer-call ledger yet fail the business outcome. Track both, never hide the mismatch.

## Close receipt

Required fields: scope_aliases, modes, coverage_status, completion_state, plan_reference, units_seen, matched, unchanged_units, unresolved_units, write_counts, verified_operation_aliases, unverified_operation_aliases, invariants, unresolved, adapter_close_status.

`units_seen` counts every distinct property unit adjudicated, including untouched units. `matched` counts units with an established existing-record identity, not number of representations. `write_counts` separates successful calls by create/update/link/merge/retire and by store; repeated successful updates to one record are multiple calls. Do not double-count one operation across verb buckets. Also record verified calls and refused/unknown attempts. When a private adapter uses different count semantics, retain its raw receipt separately and document the mapping rather than changing totals to appease validation.

A clean `verified` mutation receipt requires complete mandatory coverage, every requested postcondition read back, and no unresolved blocking invariant. A `partial` receipt may include successful verified operations while naming missing counterparts or uncertain writes. `adapter_close_status` can be not-used, accepted, refused, or unknown; an accepted administrative close does not erase unresolved business facts.

## Synthetic plan fragment

```json
{
  "unit_alias": "UNIT-A",
  "mode": "serviced-existing",
  "job_relation": "serviced",
  "identity_status": "established",
  "existence_basis": {"evidence": ["EV-MAINT"], "quantity": 1},
  "claims": [
    {"store": "hcp", "record_alias": "CARD-A", "disposition": "keep"},
    {"store": "field-intelligence", "record_alias": "ROW-A", "disposition": "keep"}
  ],
  "fields": {
    "install_date": {"current": null, "proposed": null, "evidence": [], "status": "unknown"}
  },
  "actions": [],
  "untouched_reason": "Existing linked unit; maintenance does not establish installation date.",
  "unresolved": []
}
```

This is one matched physical unit, zero creates, zero updates. The two claim entries do not justify units_seen of two. It is a fragment, not a complete transaction envelope.

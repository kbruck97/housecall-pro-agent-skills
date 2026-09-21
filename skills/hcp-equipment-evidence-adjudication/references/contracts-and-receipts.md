# Evidence contracts and read-only receipts

These are portable local interchange records, not provider request schemas. All aliases are arbitrary synthetic labels in examples. Keep the alias-to-record map in the authorized private evidence store, never in a public package or report. Null means unknown; an empty array means assessed and no qualifying rows only when coverage permits that claim.

## Input envelope

| Field | Type and constraint |
|---|---|
| `schema_version` | String, `equipment-adjudication-v1` |
| `review_key` | Opaque local alias, unique within this evidence run |
| `mode` | `installed_new`, `serviced_existing`, or `accessory_events` |
| `scope` | Object with tenant, customer, property and job aliases; each required relationship is `verified`, `ambiguous`, or `missing` |
| `policy` | Object: allowed classes, explicit exclusions, component splitting rule, accessory event rule, identity source restrictions, date proxy permission, output keys/enums |
| `coverage` | Array of collection records below; required even for no-candidate results |
| `artifacts` | Array of evidence records below |
| `existing_snapshot` | Null or scoped record set, collection time, version/checksum, pagination result; current only if refreshed for this decision |

### Collection record

`surface`: `supplied`, `public_api`, `private_alpha`, `private_react`, or `optional_private_store`.
`purpose`: logical need, such as line items, attachment metadata, originals, or equipment inventory.
`authorization`: `provided`, `authorized_read`, `opt_in_private`, or `not_authorized`.
`state`: `complete`, `partial`, `empty`, `unavailable`, `not_requested`.
`declared_total`: nonnegative integer or null; `received_total`, `unique_total`, `duplicates`, `failed`, `skipped`: nonnegative integers.
`pagination_complete`: boolean or null for non-list artifacts; `row_scope_verified`: boolean.
`gap_reason`: null or short safe explanation. Include request method/status privately; never headers or credential values.

A collection is `empty` only after a successful, scope-verified, complete enumeration yields zero true artifacts. A forbidden response is `unavailable`. A download cap makes media coverage partial. Two adapters returning the same bytes provide one artifact, not two independent witnesses.

### Evidence record

- `artifact_key`: unique alias; `kind`: `line_item`, `note`, `plate`, `context_photo`, `registration`, `worksheet`, `manual`, `equipment_record`, or `completion_metadata`.
- `source_job_key`: alias or null for customer documents; `property_tie`: verified/ambiguous/missing plus supporting alias.
- `unit_tie`: candidate alias or null, with selection rationale; `temporal_role`: proposed/performed/recommended/historical/unknown.
- `claim`: minimized assertion; avoid verbatim customer-bearing descriptions.
- `quantity_raw`: original quantity value or null; `quantity_meaning`: units/labor/bundle/unknown.
- `inspection`: inspected/metadata_only/unreadable/skipped/unavailable; `duplicate_of`: alias or null.
- `locator`: private page/row/image-region locator or sanitized artifact alias. Never serialize source URLs, filenames bearing identities, or workstation paths into public reports.

## Decision output

| Field | Contract |
|---|---|
| `candidate_key` | Unique alias; stable for this review, not a fabricated provider ID |
| `physical_role` | Supported class/component description |
| `evidence_type` | `installed_new`, `serviced_existing`, `observed_existing`, `proposed_only`, `accessory_event`, `excluded`, `unresolved` |
| `trackability` | `standalone`, `fold_into_parent`, `out_of_policy`, `unresolved`; independent of evidence strength |
| `parent_key` | Candidate alias or null; never infer an unseen parent |
| `count` | Positive integer if grouped output is allowed, otherwise one per row; null for unresolved multiplicity |
| `count_basis` | Artifact aliases plus reasoning; distinguish minimum observed from full-job count |
| `identity` | Make/model/serial each: `{value, source_keys, state}`; state is supported/unknown/conflicted |
| `classification` | Allowed enum or null, plus raw class, mapping rationale and sources |
| `install_date` | Date string or null, paired with `date_basis`: explicit/completion_proxy/unknown; never manufacture date |
| `confidence` | High/medium/low for involvement, with reason; not a substitute for per-field confidence |
| `dedupe` | Not-assessed/match/no-match/ambiguous plus snapshot alias and optional matched record alias |
| `disposition` | Include/hold/exclude with blockers and evidence keys |

Do not serialize `no-match` as `create`. A downstream writer must independently approve identity sufficiency, taxonomy, idempotency, and current scope. If a caller schema cannot express an unresolved row, exclude the row and carry the blocker in a permitted sidecar; never silently invent a resolved value.

## Verification receipt

Use `{review_key, mode, scope_verified, coverage_state, collection_snapshot_keys, candidates_considered, included, held, excluded, identity_checks, count_checks, duplicate_checks, schema_check, privacy_check, blockers, remote_writes, result_status}`.

- `result_status`: `complete_read_only`, `partial_read_only`, or `blocked`.
- Counts must reconcile to distinct candidates; repeated photos do not increment candidate counts.
- Check results use `pass`, `fail`, `not_run`, not an ambiguous boolean. Describe scope of a pass.
- `remote_writes` must be zero for this skill. Do not report a recommended change as a verified CRM change.
- External mutation verification belongs to a separate approved workflow: exact record readback, property match, changed fields, and source-job relationship. An HTTP success alone is not that receipt.

## Synthetic candidate example

```json
{
  "candidate_key": "fixture-unit-A",
  "physical_role": "heat pump",
  "evidence_type": "serviced_existing",
  "trackability": "standalone",
  "parent_key": null,
  "count": 1,
  "count_basis": {"source_keys": ["fixture-note-A"], "reason": "One named unit tested after repair"},
  "identity": {
    "make": {"value": null, "source_keys": [], "state": "unknown"},
    "model": {"value": null, "source_keys": [], "state": "unknown"},
    "serial": {"value": null, "source_keys": [], "state": "unknown"}
  },
  "classification": {"value": "heat_pump", "raw_class": "heat pump", "reason": "Explicit performed scope", "source_keys": ["fixture-note-A"]},
  "install_date": null,
  "date_basis": "unknown",
  "confidence": {"value": "high", "reason": "Completed unit-specific repair and test"},
  "dedupe": {"state": "not-assessed", "snapshot_key": null, "matched_key": null},
  "disposition": {"value": "include", "blockers": [], "source_keys": ["fixture-note-A"]}
}
```

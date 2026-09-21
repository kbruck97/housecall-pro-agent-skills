# Evidence bundle and collection receipt

These are normalized interchange contracts, not provider payloads. Integrators may add versioned fields but must not silently change enum meanings. Use null for unknown scalar facts and an explicit state for missing collections. Export aliases; maintain exact IDs only in an authorized private runtime index that is never shipped with the skill.

## Bundle schema

| Field | Type | Constraint |
|---|---|---|
| `schema_version` | string | `1.0` |
| `run_alias` | string | Unique non-identifying run label |
| `scope` | object | Tenant/customer/property aliases, `mode`, `required_surfaces` |
| `scope.mode` | enum | `single_job`, `customer_history`, `existing_record_profile` |
| `snapshot` | object | Observed start/end instants, timezone, drift flag; null in unexecuted fixtures |
| `capabilities` | array | Surface, capability, opt-in proof alias, outcome, observed schema version |
| `jobs` | array | Exact-detail-verified normalized jobs only |
| `equipment` | array | Property-gated normalized records, never page wrappers |
| `evidence` | array | Typed observations with local provenance |
| `coverage` | array | One row per required surface and object |
| `issues` | array | Code, severity, affected aliases, effect on conclusions |

### Job row

`job_alias`, `customer_alias`, `property_alias` (nullable), `property_resolution` (`explicit`, `corroborated_unique`, `unresolved`, `conflict`), `status_raw_class`, `finish_at`, `finish_basis`, `detail_state`, `source_surfaces`, `line_items`, `notes_evidence`, `attachment_aliases`, `segment_aliases`, `estimate_context_aliases`.

`line_items` contain `item_alias`, `kind`, `description_safe`, `quantity` (number/null), `quantity_semantics` (`physical`, `billing_fraction`, `unknown`), `scope_property_alias`, `evidence_aliases`. Price and payment amounts are not required for equipment evidence and are excluded from exported summaries.

### Evidence row

`evidence_alias`, `object_alias`, `source_surface`, `kind` (`performed_work`, `proposal`, `nameplate`, `registration`, `photo_presence`, `equipment_record`, `administrative`, `ui_artifact`), `observation_safe`, `field_path`, `inspection_state`, `assertion_scope`, `conflicts_with`.

The field path is a logical JSON/section locator, never a file path or URL. `inspection_state` is `text_read`, `visually_inspected`, `metadata_only`, `unreadable`, `expired_uninspected`, or `skipped`. An attachment may have several evidence observations. Registration is not synonymous with physical nameplate inspection.

### Coverage row

| Field | Rule |
|---|---|
| `object_alias`, `surface`, `capability` | Identify exact collection target |
| `state` | `pending`, `complete_nonempty`, `complete_empty`, `partial`, `unavailable`, `not_requested` |
| `required` | Boolean |
| `raw_rows`, `unique_rows`, `scope_rejects`, `pages` | Nonnegative integers for executed reads, null otherwise |
| `advertised_total`, `total_scope` | Total and population it describes; null if unavailable |
| `terminal_proof` | Explicit end/cursor/total proof, not merely a short page unless contract allows |
| `duplicate_aliases` | Repeated identities; duplicates do not count as new entities |
| `error_code` | Null or classified collection failure |

`complete_empty` requires a successful scoped parse plus terminal proof; it cannot be inferred from HTTP status alone. `unavailable` is not zero. If surface sets differ, record the intersection and each difference, then require detail review for union members. Do not require alpha/public sets to be identical when their contracts expose different statuses; require each discrepancy to be explained or marked unresolved.

## Verification receipt

Required fields: `schema_version`, `run_alias`, `status`, `scope_verified`, `required_coverage_complete`, `job_union_count`, `job_details_verified`, `equipment_scope_verified`, `media_inventory_count`, `media_inspected_count`, `media_uninspected_count`, `pagination_verified`, `privacy_check`, `write_operations`, `limitations`.

Rules:
- `status: complete` requires every required surface in a complete state and all required media actually inspected.
- `job_details_verified` equals `job_union_count` before claiming full job evidence coverage.
- Inspected plus uninspected equals the deduplicated media inventory; UI/context classification does not erase inventory entries.
- `write_operations` equals zero. Authentication refresh is not an equipment mutation, but its occurrence belongs in capability diagnostics.
- No empty-equipment claim if equipment coverage is partial/unavailable.

Synthetic example (a successful public scan with required private equipment unavailable):

```json
{
  "schema_version":"1.0",
  "run_alias":"example_partial",
  "status":"partial",
  "scope_verified":true,
  "required_coverage_complete":false,
  "job_union_count":1,
  "job_details_verified":1,
  "equipment_scope_verified":false,
  "media_inventory_count":0,
  "media_inspected_count":0,
  "media_uninspected_count":0,
  "pagination_verified":true,
  "privacy_check":"passed_on_projection",
  "write_operations":0,
  "limitations":["Required equipment capability unavailable; no empty-inventory conclusion."]
}
```

## Privacy validation

Apply an export allowlist; then recursively scan all strings, including notes, names, filenames, nested arrays, and error text. Reject credential material, URL/signature patterns, contact identifiers, physical addresses, private hostnames/paths, real record tokens, and copied raw descriptions. Review safe paraphrases for indirect identification. Hashes of raw identifiers are not automatically anonymous; prefer local non-reversible aliases with the mapping omitted. A regex pass supplements, not replaces, manual review. Do not print rejected content into validator logs.

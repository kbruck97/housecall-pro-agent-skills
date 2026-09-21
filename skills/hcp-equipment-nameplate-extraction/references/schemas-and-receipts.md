# Extraction schemas and verification receipts

The following is a local contract, not an HCP API schema. Production evidence is private. Synthetic aliases and fabricated equipment strings illustrate structure without actual record identifiers.

## Request

| Field | Required content |
|---|---|
| `request_key` | Opaque alias |
| `scope` | Tenant/property/job aliases with verified relationship state |
| `target` | Physical role, supported location or unit marker, recorded identity separately; unknown attributes null |
| `evidence_mode` | `plate_only`, `carton_enabled`, `document_enabled` |
| `comparison` | `exact` default; `normalized` only with an explicit normalization policy |
| `required_fields` | Array chosen from make/model/serial/ratings |
| `unknown_token` | Null by default; permitted caller alternatives such as empty string or `Unknown` at serialization only |
| `partial_policy` | `retain_supported_fields` or `all_unknown_on_not_found` |
| `media` | Manifest entries below |
| `output_contract` | Exact keys, enums, JSON-only flag, receipt sidecar permission |

Do not hide an incompatible contract behind a valid JSON shape. If a caller requires a full verdict but does not permit partial fields, project conservatively and preserve the partial transcription in the private ledger, not in unsupported output keys.

## Media entry

- `artifact_key`: unique alias; `source_surface`: supplied/public_api/private_alpha/private_react.
- `source_container`: attachment-specific logical field, not arbitrary webpage URL.
- `source_job_key`: alias; `target_binding`: verified/ambiguous/wrong_unit/unknown, with rationale and supporting artifact aliases.
- `kind`: unit_plate/context_photo/carton/worksheet/registration/manual/component_label/ui_asset/unknown.
- `resolution_role`: original/preview/unknown; `format`, `width`, `height`: decoded metadata or null on failure.
- `integrity`: content digest calculated with an actual hashing tool in private storage; duplicates point to the first artifact key.
- `inspection_state`: inspected/unreadable/failed/skipped; `reason`: minimized string or null.
- `transform`: orientation applied, coordinate space, crop rectangle, rotation and enhancement list; never fabricate operations.

The default coordinate space is **EXIF-oriented original pixels**, not contact-sheet or screen pixels. A crop is `[left, top, right, bottom]` within oriented image bounds. If a viewer uses raw-file coordinates, record and apply the orientation mapping explicitly instead of mixing spaces.

## Field observation

Each field holds:

`{value, state, source_keys, field_label, evidence_kind, target_binding, reason}`

- `state`: `readable`, `unreadable`, `absent`, `conflicted`, or `not_permitted`.
- `value`: exact observed string or null. Never backfill from the equipment record.
- `source_keys`: one or more inspected artifact aliases; values from documents use document provenance, not plate provenance.
- `field_label`: the visible field name, or a described manufacturer block. This distinguishes serial from part/product/job number.
- `evidence_kind`: unit_plate/carton/worksheet/registration; permitted kinds depend on mode.
- `target_binding`: verified is required to return a value as belonging to the target.
- `reason`: concise explanation of gaps or conflicts, not a raw customer note.

In plate-only mode, a logo printed on the same target manufacturer data plate may support make. A separate cabinet badge or corporate warranty header is context only. In document-enabled mode, store consumer brand and printed legal manufacturer separately if the contract permits; otherwise state the make policy before selecting one.

## Default verification semantics

Internal `status` values are `confirmed`, `corrected`, `not_found`, `partial`, `blocked`:

1. `blocked`: required media or scope cannot be accessed/verified. This is not an exhaustive no-plate finding.
2. `not_found`: the inspected permitted source set contains no target-bound legible required identity evidence, or only wrong-unit/document evidence under strict mode.
3. `partial`: target identity evidence exists but at least one required field is unknown/conflicted.
4. `confirmed`: all required fields have permitted, target-bound evidence and match recorded values under the chosen comparison policy.
5. `corrected`: all required fields have permitted, target-bound evidence and at least one differs or fills a blank recorded field.

If a caller limits verdicts to `confirmed|corrected|not_found`, agree on projection before starting. Default full-verification projection maps partial/blocked to `not_found` with a permitted reason/receipt distinguishing unreadable from inaccessible. If no such distinction can be carried and completeness matters, return a schema blocker rather than a misleading exhaustive conclusion. Some caller contracts explicitly permit partial `corrected` values; apply that contract, never assume it.

“Not found” does not authorize clearing previously recorded fields. “Corrected” is comparison output only. Installation and service involvement are intentionally absent from the strict transcription result; a separate adjudication ledger handles them.

## Synthetic complete result

```json
{
  "request_key": "fixture-request-A",
  "evidence_mode": "plate_only",
  "comparison": "exact",
  "target_binding": "verified",
  "status": "corrected",
  "fields": {
    "make": {"value": "EXAMPLE EQUIPMENT LAB", "state": "readable", "source_keys": ["fixture-plate-A"], "field_label": "Manufacturer", "evidence_kind": "unit_plate", "target_binding": "verified", "reason": null},
    "model": {"value": "DEMO H-07 X", "state": "readable", "source_keys": ["fixture-plate-A"], "field_label": "Model", "evidence_kind": "unit_plate", "target_binding": "verified", "reason": null},
    "serial": {"value": "SYNTHETIC-A-07", "state": "readable", "source_keys": ["fixture-plate-A"], "field_label": "Serial", "evidence_kind": "unit_plate", "target_binding": "verified", "reason": null}
  },
  "difference": ["Recorded model omitted the visible internal space"],
  "remote_writes": 0
}
```

## Receipt fields

Use `request_key`, `media_scope`, `declared_total`, `downloaded`, `unique_artifacts`, `duplicates`, `failed`, `skipped`, `inspected`, `target_candidates`, `selected_artifact_keys`, `rejected_candidates`, `transform_log`, `field_checks`, `target_check`, `schema_check`, `privacy_check`, `coverage_state`, `limitations`, `remote_writes`.

For each check record `pass|fail|not_run` and its scope. Totals count entries of the same kind: attachment metadata totals must not be compared to all webpage URLs. Ensure downloaded entries reconcile with unique content plus duplicates; failed/skipped originals remain in coverage. Record missing counts as null rather than zero. Do not publish an integrity hash as proof of correctness: it proves byte identity only.

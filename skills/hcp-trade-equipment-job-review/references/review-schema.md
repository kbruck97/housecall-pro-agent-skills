# Review, unit, and receipt schemas

These contracts use safe aliases in distributable examples. Exact provider identifiers belong only in an authorized runtime mapping. Null represents unknown; an export adapter may convert it to the user's required empty string or `Unknown`, never to a guessed fact.

## Review envelope

| Field | Type / rule |
|---|---|
| `schema_version` | `1.0` |
| `review_alias` | Non-identifying unique label |
| `mode` | `installed_new_review`, `physical_unit_profile`, `existing_record_profile` |
| `policy_version` | Exact approved scope version |
| `collection_receipt_alias` | Required evidence coverage receipt |
| `status` | `verified_review`, `partial_review`, `blocked` |
| `units` | Array of supported distinct physical units; not proposal candidates |
| `record_reviews` | Used for existing-record mode; one disposition per scoped record |
| `exclusions` | Counts and safe reason classes; no private raw text |
| `holds` | Unresolved candidate aliases, questions, missing evidence |
| `mutation_status` | `not_requested`, `planned`, `blocked`, `partially_verified`, `verified` |

In `existing_record_profile`, record cardinality and physical cardinality must remain separate. A single aggregate record can map to several `unit_aliases`; duplicate records can map to one unit. Do not silently drop record dispositions to enforce a one-to-one fiction.

## Physical unit schema

| Field | Type / invariant |
|---|---|
| `unit_alias` | Unique stable local alias |
| `property_alias` | Required verified service property, not billing account |
| `equipment_class`, `role` | Approved class and supported physical role |
| `trackable` | Boolean under the selected policy, not an API property guarantee |
| `relationship` | `installed_new`, `serviced_existing`, `observed_existing` |
| `installed_by_target` | Boolean; true only with actual target-job installation proof |
| `lifecycle` | `current`, `retired`, `uncertain` |
| `predecessor_alias` | Null or supported replacement link; no cycles |
| `make`, `model`, `serial` | String or null, independently evidenced |
| `install_date` | Full date or null; precision must not be invented |
| `install_period` | Null or `{value, precision, basis}` for partial year/month/range evidence |
| `install_job_alias` | Null for undocumented original installation |
| `last_service_date` | Full date or null, actual unit-specific work only |
| `service_job_aliases` | Deduplicated real work sources; inventory visits excluded |
| `evidence_aliases` | Nonempty references to collected observations |
| `field_provenance` | Map each non-null technical/date field to observation and basis |
| `existing_record_aliases` | Verified matching records; empty is valid only after complete dedupe |
| `match_state` | `matched`, `missing`, `ambiguous`, `unchecked` |
| `disposition` | `match_existing`, `candidate_missing`, `hold` |
| `unknowns`, `conflicts` | Arrays; do not hide contradictory evidence |

Required cross-field rules:

- `installed_by_target: true` requires relationship `installed_new` and target installation evidence.
- `serviced_existing` may have an original install date from a different proven install job, but never from the target service visit by default.
- Unknown original install: both `install_date` and `install_job_alias` null. A known year is `install_period`, not a fabricated first day of the year.
- `match_state: missing` requires complete, fresh live equipment coverage. Unavailable coverage means `unchecked`, disposition `hold`, even if physical existence is clear.
- Multiple existing matches require explicit duplicate/aggregate mapping, not silent selection by list order.
- `retired` requires removal/replacement evidence. A proposal alone cannot set it.
- Evidence aliases must resolve and be property-compatible. Shared evidence may support several fields, but each physical unit needs its own assignment.

## Synthetic serviced-existing unit

```json
{
  "unit_alias":"unit_A",
  "property_alias":"property_A",
  "equipment_class":"boiler",
  "role":"space_heating",
  "trackable":true,
  "relationship":"serviced_existing",
  "installed_by_target":false,
  "lifecycle":"current",
  "predecessor_alias":null,
  "make":null,
  "model":null,
  "serial":null,
  "install_date":null,
  "install_period":null,
  "install_job_alias":null,
  "last_service_date":null,
  "service_job_aliases":["job_A"],
  "evidence_aliases":["evidence_A"],
  "field_provenance":{
    "equipment_class":{"evidence_alias":"evidence_A","basis":"performed_work"},
    "role":{"evidence_alias":"evidence_A","basis":"performed_work"}
  },
  "existing_record_aliases":[],
  "match_state":"missing",
  "disposition":"candidate_missing",
  "unknowns":["Nameplate identity and exact historical service date undocumented."],
  "conflicts":[]
}
```

Assumptions for this invented example: completed performed-work text says the sole boiler was cleaned and tested, the service property is verified, and the live equipment read completed with zero records. The unit is valid for physical profiling despite blank identity and install fields. It does **not** meet the conservative installed-new write gate.

## Notes projection

When a requested external schema needs notes instead of structured fields, generate them from validated fields:

```text
Role: <supported role>
Location: <safe relative location or Unknown>
Identity: <known fields only>
Capacity: <value and basis or Unknown>
Install date evidence: <source and precision, or Not installed by this job>
Last service: <actual supported date/source, or Unknown>
Evidence: <safe performed-work or observed-presence assertion>
Unknown: <unresolved fields>
Source: <local evidence aliases>
```

Follow a user-supplied template's exact keys/order instead when required. The notes date must agree with the structured date. Do not expose private filenames, URLs, customer identity, or actual addresses in an export. An empty-array-only response is valid only after verified supported-empty review, not when evidence is blocked.

## Review verification receipt

Required: `review_alias`, `mode`, `coverage_status`, `policy_version`, `property_scope_verified`, `supported_physical_count`, `existing_record_count`, `record_dispositions_count`, `current_count`, `retired_count`, `uncertain_count`, `hold_count`, `field_provenance_checked`, `replacement_graph_checked`, `date_semantics_checked`, `schema_valid`, `privacy_checked`, `write_operations`, `mutation_status`, `limitations`.

Counts must reconcile: current + retired + uncertain equals supported physical count. Existing-record mode requires existing record count equals record dispositions count, including holds/exclusions. Do not force physical count to equal record count. `verified_review` requires required coverage and all checks; unresolved candidate holds must be disclosed and prevent a blanket verified claim for those candidates. A verified read-only review has `write_operations: 0` and `mutation_status: not_requested`.

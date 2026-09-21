# Fact and receipt schema

These contracts describe evidence handling, not an API payload. All fields below are required unless explicitly nullable. Source references are sanitized aliases resolved by the authorized operator.

## Request

| Field | Type | Meaning |
|---|---|---|
| request_alias | string | Invented or sanitized work reference. |
| model_literal | string | Original model as supplied; preserve punctuation and suffix. |
| brand_literal | string or null | Nameplate brand, not automatically a corporate parent. |
| target_field | enum | filter_size, capacity, cabinet_width, model_family, manual, refrigerant, fuel, or other explicitly named quantity. |
| fact_scope | enum | product-specification, compatible-accessory, installed-configuration. |
| quantity_kind | string or null | For capacity specify circuit and input/output/nominal/rated. |
| context | object | Relevant cabinet/orientation/region/fuel/accessory evidence, each nullable with reason. |
| retrieval_mode | enum | supplied-documents, authorized-local, authorized-online. |
| output_contract | object | format, allowed_unknown_token, allowed_not_applicable_token, units, citation_allowed. |

## Evidence entry

| Field | Type / constraint |
|---|---|
| source_alias | Unique string. |
| source_class | manufacturer-manual / manufacturer-product-data / manufacturer-index / distributor-document / installed-label / other. |
| title, issuer, revision | Strings; revision nullable with explicit limitation. |
| locator | Page, table, literal model row, column, footnote; no private retrieval address. |
| inspected | Boolean; false entries cannot support a final fact. |
| exact_model_text | Literal source text. |
| applicability | exact / documented-family-member / uncertain / mismatch. |
| applicability_basis | Which table or nomenclature ties the input to this source. |
| fact_literal | Exact relevant value and quantity label; null when absent. |
| limits | Configuration, test conditions, age/revision, missing variant, or source access limits. |

## Fact result and receipt

`result` contains status (SUPPORTED, UNKNOWN, NOT_APPLICABLE), value (nullable), units (nullable), quantity_kind, fact_scope, evidence_aliases, conflict_aliases, unknown_reason, and installation_claim (always false for generic reference lookup).

`verification` contains literal_preserved, applicable_model_confirmed, table_headers_checked, footnotes_checked, scope_matches_question, conflicts_resolved, source_reopened, arithmetic_verified (not-needed/yes/no), network_used, crm_writes (always zero), and rendered_answer.

Validation rules:

- SUPPORTED requires a non-null value and at least one inspected applicable source with the exact requested quantity. An index containing only a family name cannot support filter size.
- UNKNOWN requires null value and an actionable reason, not a guessed range hidden in notes.
- NOT_APPLICABLE requires evidence that the property truly does not apply; no evidence is not non-applicability.
- All non-null fields derived from literature retain source aliases. Family ranges must be labeled ranges; a range cannot satisfy an exact-member question.
- A restrictive output contract affects only rendering. It does not remove internal evidence or turn UNKNOWN into an actual equipment field value.
- `crm_writes` must remain zero; later profile enrichment is a separate approved transaction.

## Synthetic receipt fragment

```json
{
  "model_literal": "DEMO-F60-CB(NG)",
  "target_field": "filter_size",
  "fact_scope": "installed-configuration",
  "result": {
    "status": "UNKNOWN",
    "value": null,
    "units": null,
    "quantity_kind": "installed filter dimensions",
    "fact_scope": "installed-configuration",
    "evidence_aliases": ["DOC-FACTORY-RACK"],
    "conflict_aliases": [],
    "unknown_reason": "Factory manual lists multiple arrangements; installed cabinet is unidentified.",
    "installation_claim": false
  },
  "verification": {
    "literal_preserved": true,
    "applicable_model_confirmed": true,
    "table_headers_checked": true,
    "footnotes_checked": true,
    "scope_matches_question": false,
    "conflicts_resolved": true,
    "source_reopened": true,
    "arithmetic_verified": "not-needed",
    "network_used": false,
    "crm_writes": 0,
    "rendered_answer": "UNKNOWN"
  }
}
```

The source may be model-applicable while failing installed-scope applicability. This distinction explains why reading the correct manual can still produce UNKNOWN. The fragment is not a complete request/evidence bundle.

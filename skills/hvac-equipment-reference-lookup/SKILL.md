---
name: hvac-equipment-reference-lookup
description: Use when looking up HVAC model-specific facts. Verify manuals and applicability; distinguish product specifications from installed-site evidence.
license: MIT
version: 1.0.0
---

# HVAC equipment reference lookup

Answer model-specific questions about filter dimensions, capacity, cabinet width, model families, manuals, refrigerant, or fuel configuration without turning likely conventions into facts. This is read-only research, not equipment reconciliation, commissioning advice, or authorization to change a customer profile.

## Preflight

1. Capture the exact supplied model string, visible suffixes, manufacturer/nameplate brand, requested fact, units, and required response format. Preserve the original token; an OCR correction is a separate candidate requiring evidence.
2. Decide the fact scope: published product specification, compatible accessory, or actual installed configuration. Ask for the smallest missing discriminator when it changes the answer. If the requested format permits only a value or UNKNOWN, abstain rather than add a question.
3. Establish permitted evidence sources. With no network permission, use only supplied or authorized local documents and report their limitations. Do not imply a current lookup occurred. With permission, prefer manufacturer literature and retain document/version/page provenance. Customer-specific evidence is not required for a generic product lookup.
4. For CRM-derived inputs, public HCP reads are tenant-capability dependent; private alpha is separately opt-in and Field Intelligence is optional. This skill requires neither private surface and performs no writes. Private `equipment_*` names are adapter contracts, not public APIs or promised tools.

Use [lookup protocol](references/lookup-protocol.md) and [fact and receipt schema](references/fact-and-receipt-schema.md).

## Procedure

1. **Separate identity from discovery.** Search the exact model first when online research is allowed; broaden to a documented family only when the exact SKU is absent. Keep the exact suffix and a rationale for each candidate family. Do not silently collapse near-identical generations or refrigerant families.
2. **Find primary documentation.** Use manufacturer installation instructions, product data, technical manuals, and exact-model tables before reseller summaries. Product indexes, sitemaps, structured metadata, and text-only variants can locate documents; discovery metadata alone is not evidence for an unstated dimension.
3. **Check applicability.** Confirm family, model row, cabinet width, orientation, region, fuel/electrical variant, document revision, and footnotes as relevant. A stale page title must not override a clearly identified model table; contradictory metadata still requires resolution.
4. **Read the actual table.** Preserve row/column headers and footnotes; visually inspect scanned or broken extraction if needed. Do not cite a search snippet as though the PDF was read. When a table spans pages, inspect continuation labels before attaching a value to a model.
5. **Keep quantities semantically separate.** Distinguish heating input, heating output, cooling nominal capacity, rated capacity, blower airflow/range, and domestic-hot-water input. A furnace's blower compatibility is not its heating capacity or proof of the attached cooling system's tonnage. Use documented nomenclature, not a generic numeric-suffix guess.
6. **Handle installation-dependent facts.** A manual's allowed rack does not establish the customer's field-installed filter cabinet or return-grille size. A modified return makes predecessor filter photos unreliable. Preserve exact plate fuel suffix even if separately documented conversion changes the installed fuel configuration.
7. **Adjudicate conflicts.** A family page may establish a range but not the exact member's rating. Product references establish design facts, not unit serial, installation date, installed count, or proof of new installation. A serviced-existing unit remains serviced-existing after enrichment; lookup does not change work semantics.
8. **Verify and answer.** Reopen the cited source location, confirm exact applicability and requested quantity, and build the receipt before rendering the answer. Report supported facts with scope and citations when permitted. When instructed to return only a size or UNKNOWN, output precisely that value/token without explanation; keep evidence in the work record, not merely in memory.

## Stop conditions

Return UNKNOWN for ambiguous model mapping, unreadable decisive tables, missing installation-specific evidence, unresolved source conflict, unsupported suffix decoding, inaccessible required sources, or a family range where an exact rating is requested. Do not substitute a nearby model or a guessed filter dimension. NOT_APPLICABLE is distinct from UNKNOWN and may be used only when demonstrated and the output contract allows it.

## Verification receipt

Record exact input, candidate mapping, requested quantity/scope, sources actually inspected, applicable rows/footnotes, result status, value/units, unresolved limitations, retrieval mode, and final output format. See the schema and synthetic cases below. A successful retrieval proves access, not correctness; source applicability must also pass. No CRM mutation receipt is produced by this skill.

Companion skills hcp-equipment-nameplate-extraction and hcp-equipment-evidence-adjudication can resolve unit evidence; hcp-equipment-profile-reconciliation handles a separately authorized write plan.

## References

- [Lookup protocol](references/lookup-protocol.md)
- [Fact and receipt schema](references/fact-and-receipt-schema.md)
- [Synthetic cases and failure modes](references/synthetic-cases.md)
- [Editorial source decisions](references/source-decisions.md)

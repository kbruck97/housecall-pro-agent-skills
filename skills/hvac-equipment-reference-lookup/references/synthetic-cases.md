# Synthetic cases and failure modes

Every product token, source title, and rating here is invented for testing. They are not real product specifications or recommendations.

| Fixture | Required answer or behavior | Failure mode |
|---|---|---|
| DEMO-F60-CB manual identifies one factory rack row as nominal 16 × 25 × 1 inches; question specifically asks that factory row | Return that size with factory/nominal scope when prose is allowed; exact size only under size-only contract. | Conflating factory specification with actual installation. |
| Same model, question asks field-installed cabinet; cabinet unknown | UNKNOWN; request cabinet label if response contract permits. | Guess from furnace capacity. |
| DEMO-COMBI-Q table labels heating input 90,000 BTU/h and DHW input 170,000 BTU/h | Keep separate labeled values; neither is automatically heating output. | Largest number used as generic capacity. |
| Model DEMO-HP-A appears only in an index; index links a family page | Use index for discovery, continue to literature for refrigerant or exact capacity. | Discovery metadata promoted to a specification. |
| DEMO-HP-A and DEMO-HP-B are adjacent generations with different refrigerants | Reject B's refrigerant as support for A; UNKNOWN until A source found. | Near-model substitution. |
| Exact label DEMO-COMBI-Q(NG), verified conversion record mentions other fuel | Preserve literal model; describe configuration separately if asked. | Editing suffix to match field conversion. |
| A model-like OCR token could contain letter O or digit zero | Keep both candidates unresolved; request plate evidence. | Silent identifier repair. |
| Manual extraction loses table columns or footnotes | Inspect page image; if unavailable, UNKNOWN. | Correct number attached to wrong row. |
| Public product page says family heating range, exact member rating absent | Report family range only for a family question; exact member question UNKNOWN. | Family maximum assigned to every model. |
| Source job only serviced an existing unit; literature confirms its type | Reference enrichment only; no new-install claim or installation date. | Product identification changes work semantics. |
| Network unavailable, supplied document sufficient | Answer from supplied document with retrieval_mode supplied-documents and network_used false. | Claiming live manufacturer verification. |
| Network unavailable, decisive document absent | UNKNOWN with access limitation when allowed. | Fabricated source receipt. |
| Output contract is value or UNKNOWN only, evidence is ambiguous | Exactly UNKNOWN, no explanatory suffix. | Correct abstention invalidated by output formatting. |

## Receipt review exercise

For each fixture, check the target quantity and scope before the source value. Reject a receipt if it contains a precise fact without an inspected applicable source, a converted value without a recorded calculation, a changed model literal without evidence, or a CRM write. Positive tests require explicit source applicability; negative tests require a concrete evidence gap rather than a generic confidence score.

# Synthetic adjudication and failure tests

All examples are invented, not sanitized historical customers. Use aliases only. Test the selected mode and policy together; identical input can correctly produce different output under installed-new review versus physical profiling.

| Evidence | Correct decision | Error this catches |
|---|---|---|
| Completed text: “Cleaned and tested the sole boiler”; no plate or install history | One serviced-existing profile unit, unknown identity, blank install fields | Reject all service-only units or invent an installation |
| Same boiler evidence in installed-new mode | No new installation supported | Treat completion as installation |
| Scheduled proposal with paid deposit and exact models, no performed work | No physical installed-new rows; proposal retained as context | Payment equals installation |
| Completed job contains only tax, material pickup, permits | Supported empty equipment set after complete coverage | Completed status manufactures assets |
| Completed installed furnace, two duplicate fractional billing jobs | One furnace, all provenance retained; date from actual completion evidence | Fractions become units or arbitrary date |
| Completed diagnostic photographs old outdoor unit; later replacement proves different model | Old/new identities separated, indoor heads retained if not replaced | Old plate copied to new outdoor unit |
| Maintenance proposal recommends replacing two condensers | Existing condensers remain current | Retirement from recommendation |
| Separate photos identify same model but different serials | Distinct physical units | Model-only dedupe |
| Same serial appears under two service properties | Hold identity/scope conflict | Cross-property merge |
| One aggregate ductless record represents outdoor plus two heads | Three supported units with aggregate mapping | Force one record per unit or duplicate silently |
| Record name is “Humidifier”; new evidence is a dehumidifier | Distinct class; do not substring-match | Similar text suppresses a real unit |
| Live matching placeholder exists although prompt says none | Match/enrichment proposal, not create | Trust stale canonical emptiness |
| Private equipment read unavailable, installation otherwise clear | Supported installed unit, match unchecked, write hold | Missing access equals missing record |
| Visible water heater unrelated to target service in wide room photo | At most observed-existing if requested and property verified; not installed/serviced | Incidental photo expands job scope |
| Installed standalone hydronic zone circulator, parent boiler undocumented | One permitted circulator, no invented boiler | Every pump implies parent installation |
| Geothermal loop-pump repair | Parent service evidence if parent is proven; no separate flow-center candidate | Components inflate asset count |
| Installed thermostat and control board under conservative exclusions | No independent rows, including accessory mode | Old examples override current exclusions |
| Imported job has another property's boiler under a separate section | Exclude that assertion from target property | Container customer attribution hides off-property work |
| Only a year is documented for installation | Partial install period; no full date | Invent month/day |
| Registration readable, task requires physical plate verification | Hold plate verification; preserve registration evidence separately | Paperwork becomes plate proof |
| Bare plural “ductless heads serviced” without count | Count hold, no fabricated exact head count | Minimum plural treated as exact count |
| Completion text specifies one combi boiler with domestic hot water | One appliance, two roles unless separate tank is proven | Roles become duplicate units |

## Worked profile versus mutation

Evidence_A says the sole boiler at property_A was cleaned and tested. The job is complete, but its imported timestamp is not a trustworthy physical service date. Live equipment coverage is complete and empty. No plate is available.

- Physical-unit mode: unit_A is `serviced_existing`, current, with unknown make/model/serial, install date null, and service date null. Cite evidence_A and explain date uncertainty.
- Installed-new mode: no unit was proven installed by this job.
- Mutation handoff: no installed-new create plan. An explicitly approved serviced-existing backfill could be considered only under a policy allowing unknown identity, with fresh dedupe and exact readback.

## Worked replacement with an ambiguous aggregate record

Evidence_B proves an outdoor unit was replaced while the existing indoor head remained. Evidence_C is a photo of the failed outdoor unit. Record_A is named only “Ductless system” and has no usable identity fields.

Build current outdoor and retained indoor physical units plus a retired outdoor only if requested. Assign evidence_C to the retired outdoor, not the replacement. Record_A may be aggregate; mark the record mapping ambiguous until its job links/notes and current state establish its meaning. Do not create multiple replacement records to resolve the ambiguity. Receipt physical count and existing record count separately.

## Failure-oriented verification

Validate all enum values, required keys, count equations, null/date semantics, evidence resolution, property matches, policy exclusions, replacement graph acyclicity, and output serialization. For strict JSON requests, parse the actual final array and ensure no surrounding prose. Test blocked collection separately from supported empty results. For mutations, use an adapter test environment or a separately approved bounded live action; never treat these invented cases as execution receipts.

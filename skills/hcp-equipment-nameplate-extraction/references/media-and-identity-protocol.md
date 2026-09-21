# Media, target binding and ambiguity protocol

## Evidence eligibility by mode

| Source | Plate-only | Carton-enabled identity | Document-enabled profile |
|---|---|---|---|
| Target unit official readable data label | Primary | Primary | Primary identity evidence |
| Same-unit additional official serial sticker | Eligible after same-cabinet and field-role proof | Eligible | Eligible |
| Manufacturer logo on that data plate | Make only if legible | Make only | Make evidence |
| Separate cabinet badge | Target context, not strict make | Context unless explicitly permitted | Possible consumer-brand evidence with same-unit proof |
| Carton label | Excluded | Conditional: unique target tie and explicit permission | Conditional identity, never installation proof |
| Unit-specific registration | Context | Corroboration | Eligible if target/serial/date tied; preserve conflicts |
| Dated maintenance worksheet | Context | Context | Service and transcribed identity if legible and tied |
| Generic brochure/manual | Reference only | Reference only | Family/spec reference only after independent identity tie |
| Neighboring compressor/control/pump label | Wrong target unless that component is requested | Same | Same |
| UI logo/avatar/map icon | Not equipment evidence | Not equipment evidence | Not equipment evidence |

A source can establish service while failing nameplate verification. A completed unit-specific worksheet supports serviced-existing inventory, with null installation date; it yields no plate-only confirmation. Conversely, a crisp plate establishes identity without proving the current job installed or serviced the unit.

## Target-binding checklist

1. Identify requested role before looking for the most readable label.
2. Establish property and job provenance; a same-customer artifact from another property is not transferable.
3. Locate candidate cabinets/components in context views. Use observed unit markers, cabinet features and physical continuity, not invented room assignments.
4. Associate each close-up with a candidate. Same-job membership alone is weak when several identical units exist.
5. Compare entire model and serial, including final characters, across siblings. Same-model different-serial units stay distinct.
6. If the recorded values match an indoor head but the request targets outdoor equipment, reject the indoor match. Recorded errors must not redefine the target.
7. If a target-specific plate differs from recorded values, it can support correction. If the only legible plate is a different unit, it cannot.

Two separate labels may be combined only when both belong to the same physical target and the field meanings are explicit. A heat-exchanger certification serial, compressor serial, or product code may differ from the appliance serial legitimately. Do not automatically overwrite or concatenate them. If field semantics cannot be established, preserve both observations as a conflict.

## Bounded image-reading sequence

- Inspect original metadata and apply orientation before any coordinate selection.
- Make one context view and one identity-field crop, adding a revised crop if the first misses the actual plate.
- Correct crop rotation/perspective where useful; keep the transform record and the unaltered original.
- Compare raw color with a small number of nondestructive contrast/grayscale/sharpen views. Enhancement is a viewing aid, not new evidence.
- If an ambiguous character remains, inspect another original view of the same label. OCR agreement is not independent corroboration if every engine sees the same blur.
- Stop after the available views and reasonable crop variants cannot distinguish the characters. Request a straight-on close-up of the target label, plus a wide unit-location view if binding is ambiguous.

Never use generative reconstruction, model-family expectations, neighboring serial sequences, or a plausible manufacturer prefix to complete text. Preserve an internal uncertainty note such as “final character ambiguous between letter and digit,” but output null/unknown for the field when the schema needs an exact value.

## Barcode and OCR safeguards

OCR and barcode tools are optional, locally discovered capabilities. State whether they were used. A barcode must be on the same selected label, in a field whose payload meaning is established. Product identifiers and serials can have different prefixes or omit suffixes; do not strip or concatenate bytes unless the label schema documents that interpretation.

For strict human-readable extraction, use barcode decoding only to corroborate legible text. If the caller explicitly allows machine-readable identity, retain decoded and human-readable observations separately and label their provenance. If they disagree, do not pick the more convenient one. A QR code on a controller, marketing link, or component is not the parent unit's serial.

## Strings, dates and specifications

- Preserve explicit model rows rather than combining a product-family header with the model.
- Keep product/part numbers separate from serials; a long barcode caption is not necessarily serial.
- Do not confuse form-box borders with hyphens or collapse printed internal spaces in exact mode.
- Exact mode uses the printed manufacturer block, including case and legal suffix when visible. Normalized brand mapping requires explicit permission and separate evidence; no silent case-by-case exceptions.
- Manufacturing date, commissioning date, service date and installation date are different claims.
- Capacity must be an explicit labeled plate rating or separately documented exact-model specification. Measured amperage, filter size, refrigerant weight and model digits alone do not establish it.
- Plate documentation is private evidence. If derivatives are shared, remove unrelated text, faces, location metadata and private filenames without erasing the source field under review. Do not publish whole service documents to explain a three-field result.

## Failure modes and recovery

| Failure | Safe response |
|---|---|
| Thumbnail readable-looking but original missing | Do not claim full-resolution verification; ask for original or mark limitation |
| Original has no extension | Check decoded type; do not silently discard |
| EXIF crop lands on blank cabinet | Recompute oriented coordinates and recrop before unreadable conclusion |
| Glare hides last serial digit | Alternate same-unit view; if unresolved, serial unknown |
| Only registration matches recorded values | Strict not-found; document-enabled result separately sourced |
| Sibling plate is clearer | Reject sibling as correction source |
| Several conflicting official labels | Determine role/field meaning; otherwise field conflict |
| Expired media link | Request authorized metadata refresh, not session harvesting |
| Unauthorized private collection | Stop collection; retain supplied-file results with coverage limits |
| No readable plate but completed service note | No strict identity result; refer involvement to evidence adjudication |

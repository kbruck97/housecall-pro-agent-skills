---
name: hcp-equipment-nameplate-extraction
description: Use when reading HCP equipment plates. Transcribe exact target-unit identity with provenance and explicit unknowns.
license: MIT
version: 1.0.0
---

# Equipment nameplate extraction

Extract make, model, serial and explicitly requested ratings from a specific physical unit's readable manufacturer label. The deliverable is a transcription or verification result, not a CRM update. A clear plate from the wrong unit is worse than an unknown field.

## Preflight: choose the evidence contract

1. Confirm the authorized job/property scope and target physical role: indoor head, outdoor unit, boiler, tank, coil, controller, or another identified unit. Record location/zone/unit number when genuinely known. A recorded model/serial is a comparison hypothesis, not proof of target identity.
2. Choose **strict plate-only** (default), **explicit carton-enabled identity**, or **document-enabled profile review**. Do not silently mix them. A carton can support identity only when expressly accepted and independently tied to the target; it never proves installation. Worksheets/registrations may support a profile review but cannot masquerade as inspected physical plates.
3. Choose exact-character or explicitly permitted normalized comparison. Default to exact printed characters. Keep raw manufacturer text separate from consumer brand; do not import a corporate-family or registration-program name into make by assumption.
4. Confirm output schema, unknown token, required fields, partial-field policy, and whether a JSON-only projection is required. The default internal result contract is in [schemas and receipts](references/schemas-and-receipts.md). Never claim full confirmation when the caller requires fields that remain unreadable.
5. Inventory supplied media and capabilities: full-size originals, attachment manifest, image viewer, crop/rotation tools, optional OCR/barcode decoder, and safe local output storage. No OCR package or universal HCP fetch tool is bundled here. Missing tooling narrows the result; do not claim it ran.
6. For live evidence collection, discover the authorized public adapter first for the needed capability. Private alpha/React sources are **opt-in**, not public API guarantees. Validate tenant context and read scope before use; missing access is a blocker, not permission to rummage for sessions. For offline requests, inspect only supplied/authorized local material and make no network calls.

## Procedure

1. **Build the media manifest.** Record job/artifact aliases, source container, original-versus-preview status, format, dimensions, inspection state, and provenance. Include user-supplied images where authorized. Attachment collections can be empty, partial, unavailable, or complete; distinguish them.
2. **Reconcile source inventories.** If authorized collection exposes public attachments and private alpha/React attachment containers, compare them without counting UI assets. Stable artifact identity and content hashes collapse duplicate downloads; signed-link query strings do not establish new photos. A source count mismatch requires a gap note, not invented images.
3. **Acquire originals safely.** Prefer the provider's explicit original field, not arbitrary URLs from a page. Verify decoded content and dimensions; extensionless originals can be images, and an original can be small. Keep authentication on its approved service origin; third-party signed downloads use a fresh unauthenticated client with redirect validation. Do not publish signed URLs or raw filenames.
4. **Orient and triage.** Decode the original, apply EXIF orientation, and create a labeled contact sheet only for selection. Preserve an unmodified original. Map every thumbnail label to its artifact key; never infer target mapping from contact-sheet order. Final extraction uses the original or a traceable crop, not the contact sheet.
5. **Bind target before reading values.** Connect the close plate to the requested cabinet/component using a shared photo, recognizable cabinet/context continuity, explicit unit/location markings, or other independent evidence. Compare all plausible siblings. The target role wins over a tempting exact match to possibly wrong recorded values. Same model alone is insufficient.
6. **Inspect and crop.** Read the full label once, then crop the identity fields from oriented original coordinates. If a crop misses the label, rebuild an orientation-aware coordinate grid and recrop. Rotate/deskew the crop; compare raw color with modest contrast/grayscale/sharpen variants. Do not use generative filling or infer characters from expected model formats.
7. **Transcribe field labels and values.** Prefer explicit Model/M/N and Serial/S/N rows over product-family headers, product numbers, part numbers, certification IDs and manufacturing codes. Preserve letters, zeros, hyphens, internal spaces, punctuation, case, and legible suffixes. Distinguish printed field formatting from ambiguity; do not normalize by habit.
8. **Cross-check ambiguity.** Compare alternate views of the same target, not its sibling. Same-label barcodes may corroborate only when role and payload semantics are established. A decoder result is not permission to fill unreadable human text in strict human-readable mode. Conflicting same-unit labels remain field conflicts until resolved. See [media and identity protocol](references/media-and-identity-protocol.md).
9. **Apply field-wise eligibility.** A legible make does not make model/serial readable. A worksheet, badge, nearby label or existing record cannot fill strict plate-only gaps. Document-enabled review must label those alternative sources and preserve uncertainty. Manufacturer capacity lookup is a separate evidence step; operating amps or charged refrigerant weight are not nominal capacity.
10. **Compare and serialize.** Retain observed values separately from recorded values. Produce the chosen verdict only after target binding and required-field checks. Return exact keys and unknown values requested by the caller. With JSON-only requests, emit no prose/fences; keep a receipt in a permitted sidecar rather than adding undeclared keys.

## Stop conditions

Stop transcription for a field when it stays unreadable after a bounded crop pass; report unknown with a reason. Stop full verification when the only legible plate belongs to a sibling, the component role conflicts, a label cannot be tied to the target, all evidence is paperwork under strict mode, or required originals are inaccessible. Stop collection on authorization failure rather than searching for another tenant's session. Preserve accessible evidence but mark incomplete coverage.

Do not copy recorded values into unknowns, guess serial tails, decode model capacity without documentation, or treat a casing change as a physical equipment change. Do not infer installation date from the plate's manufacture date or job's service date.

## Verification and handoff

- Reopen the selected original/crop and check every returned character against the cited field.
- Verify target role and component association independently of recorded identity values.
- Check sibling plates were excluded; same bytes are one source, not corroboration.
- Check each returned field has permitted provenance and every unknown has a reason.
- Validate required fields, verdict, JSON syntax, exact keys and unknown token.
- Record which image/OCR/barcode operations actually ran; a readable artifact or manual review is not a claimed automated test.
- Export aliases and minimized rationale only. Remove names, contacts, addresses, original filenames, location metadata, hostnames, credentials and signed links from shareable receipts.
- State zero remote writes. “Corrected” means an extraction differs from recorded text, not that any equipment record was changed.

hcp-equipment-evidence-adjudication decides installed-new versus serviced-existing involvement. A plate establishes identity/existence, not work performed. hcp-alpha-data-collection is an optional collection dependency with private adapters explicitly enabled. hcp-equipment-profile-reconciliation is a separately authorized write workflow; this package neither invokes nor simulates its tools.

## References

- [Schemas and receipts](references/schemas-and-receipts.md)
- [Media and identity protocol](references/media-and-identity-protocol.md)
- [Synthetic acceptance cases](references/synthetic-cases.md)
- [Source decisions](references/source-decisions.md)

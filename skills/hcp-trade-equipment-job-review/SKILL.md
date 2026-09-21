---
name: hcp-trade-equipment-job-review
description: Use when reviewing HCP jobs or equipment profiles to separate installed-new, serviced-existing, proposals, and distinct physical units.
license: MIT
version: 1.0.0
---

# Evidence-led trade equipment review

Produce an auditable equipment review from scoped evidence. Read-only is the default. A candidate marked missing is a recommendation, not a new HCP record. This package includes no mutation tool, authenticated session helper, or guaranteed provider endpoint.

## Preflight: choose the output before choosing the gates

| Mode | Output unit | What the result means |
|---|---|---|
| `installed_new_review` | One distinct unit installed by the target job/project | Creation eligibility requires installation proof, service-property proof, identity, complete live dedupe, and separate approval |
| `physical_unit_profile` | One distinct supported physical unit across the requested history | May include serviced-existing or observed-existing units with unknown identity and blank install fields |
| `existing_record_profile` | One review row per existing in-scope record | Describes records, which can aggregate several physical units or duplicate one unit; does not change cardinality automatically |

1. Confirm tenant, exact job/customer/property scope, mode, source freshness, output schema, privacy audience, and whether retired units or permitted accessories are requested. If a schema forces an unknown fact into a false certainty, stop and request a representable contract.
2. Require a completed collection receipt. Use hcp-alpha-data-collection for scope-safe collection; only actual configured capabilities may be invoked. Public job reads are preferred where available. Private alpha/React and equipment adapters require explicit opt-in; missing equipment reads block safe-to-create conclusions.
3. Load the approved taxonomy policy using [Scope and evidence rules](references/scope-and-evidence.md). Distinguish explicitly excluded classes, folded components, optionally reportable accessories, and trackable parent units. A request for “everything” does not silently lift exclusions.
4. Validate identifiers before lookup. Require an exact property linkage; reject placeholders and billing-only destinations. Null linkage may be resolved only by a unique corroborated service address within the verified customer. Mixed imported line-item sections require separate property attribution.
5. Confirm no mutation authority is implied by words such as review, profile, missing, new, or reconcile. Keep evidence analysis and mutation planning separate.

## Procedure

1. **Build the evidence ledger.** For a target job, read details, direct line items, actual completion/service dates, notes, and attachment inventory. For customer profiles, review all scoped jobs and all requested service properties, not only jobs already attached to equipment. Read existing equipment details and job links. Keep unavailable evidence distinct from empty evidence.
2. **Classify performed work before extracting identity.** Tag each assertion as installed-new, serviced-existing, observed-existing, proposed, removed, or unsupported. A completed status without specific work is insufficient; a scheduled status with independent completed work evidence is a conflict to document, not an automatic rejection of all presence/service evidence. Deposits, material lists, approved proposals, and job titles do not prove installation.
3. **Build physical units, not invoice rows.** Use explicit quantities, distinct nameplates, location/role, and unit labels. Deduplicate repeated maintenance and progress-billing rows. Group verified composite segments but preserve each artifact's source. Do not count invoice fractions, photographs, cooling zones, capacity, or repeated records as unit counts.
4. **Separate predecessor and replacement.** A removed old unit and its replacement are distinct identities. Do not copy the old nameplate onto the new unit. A planned replacement neither retires the current unit nor proves a new one. Retain old units only in requested replacement-aware profiles with removal evidence. Temporary relocation is not a new install.
5. **Extract each field with provenance.** Use installed-unit evidence for model/serial; keep nameplate and registration sources distinct. Respect plate-only requests. Make is the supported equipment brand, not a corporate family, supplier, registration administrator, or component maker. Unknown fields remain null/blank as the requested schema specifies. Derived capacity requires an approved, cited technical source; do not decode model prefixes from memory.
6. **Assign dates conservatively.** Set installation date only from actual installation/commissioning evidence for this physical unit. Completion may be a labeled date basis when the exact job clearly installed it. Service-only dates never become installation dates. Import-created, planned, paid, and repeated billing timestamps are not physical work dates. If only a year or uncertain range is known, preserve that precision rather than inventing a day.
7. **Match current records.** Re-read live property equipment even if a prompt claims an empty canonical set. Match by exact serial with compatible role/type and property, then corroborated tracking identity, then sufficiently discriminating model/location/topology. Same-model siblings and cross-property serial conflicts require review, not automatic merge. Generic names, similar capacity, or substring matches cannot suppress distinct assets.
8. **Choose a disposition.** Use `match_existing`, `candidate_missing`, `hold`, `exclude`, or `unsupported`. A matched placeholder may be proposed for enrichment, never blindly replaced by a duplicate. Distinct physical rows may refer to one aggregate record; flag that mapping rather than pretend it is one-to-one. See [Review schema](references/review-schema.md).
9. **Apply mode gates.** Installed-new review requires actual installation and adequate unit identity for a mutation proposal. Physical-unit profiling can legitimately retain a clearly serviced boiler with unknown make/model/serial and no installation date. An existing-record profile must not silently invent additional rows from adjacent photos. Every existing scoped record gets an accounted-for disposition, even when it is excluded or ambiguous.
10. **Verify and hand off.** Check evidence-to-field provenance, scope, physical versus record cardinality, replacement chains, dates, exclusions, live matches, and strict schema. Produce the requested output plus the allowed receipt, or a separately retained receipt when JSON-only output is required. Follow [Mutation handoff](references/mutation-handoff.md) only after explicit write authorization and a configured adapter; do not run changes as part of a review.

## Stop conditions and honest outcomes

- **Blocked:** tenant/property ambiguity, malformed identifiers, unavailable required evidence, unreadable required media, incomplete pagination, unknown adapter, or missing permission. Do not respond with an empty array that implies a completed review.
- **Hold per candidate:** unresolved identity/count/replacement/date conflict or uncertain live match. Preserve unaffected candidates without marking the whole review fully verified.
- **Supported empty set:** completed scoped evidence review finds no permitted physical units. For strict JSON-only requests, return exactly `[]`; retain the receipt through an approved channel, not as extra text.
- **No new installation supported:** valid conclusion for serviced-existing work, not a claim that the property has no equipment.
- **No mutations:** the normal outcome, including a review that recommends missing records. Report “created” only after exact post-write readback and source-job linkage verification.

## References and dependencies

Read [Scope and evidence rules](references/scope-and-evidence.md), [Review schema](references/review-schema.md), [Mutation handoff](references/mutation-handoff.md), and [Synthetic cases](references/synthetic-cases.md). Editorial conflict resolutions are in [Source decisions](references/source-decisions.md).

Related skills, if installed, are hcp-alpha-data-collection, hcp-equipment-nameplate-extraction, hcp-equipment-evidence-adjudication, hcp-equipment-profile-reconciliation, and hvac-equipment-reference-lookup. Their names are routing guidance, not guaranteed tools or authorization to write.

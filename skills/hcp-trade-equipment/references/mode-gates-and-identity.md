# Mode gates and physical identity

## Installed-new: strict creation lane

Require each of the following for a create candidate:

1. Independently supported completed installation scope for this unit. Use tenant-documented completion statuses plus performed-work evidence. Payment alone is not completion. A scheduled/canceled record or an accepted proposal alone cannot satisfy the gate.
2. A resolved real service property and exact customer membership.
3. Specific installed-unit evidence: a completed installation narrative, identifying line description, plate, matched registration or equivalent source. Generic labor categories with no identity support fail this lane. Zero notes plus zero attachments is not alone a blocker when direct line descriptions carry sufficient completed installation identity; conversely a large attachment count is not proof.
4. Enough unit-specific identity to distinguish the asset under the configured strict create policy. Do not manufacture make/model/serial; a serial may legitimately be unknown, but a generic category alone is not a strict identity-backed create.
5. Current-state inventory checked completely enough to exclude a duplicate or supported placeholder match.

The result may be mixed: create one supported unit, enrich another, hold a third. Do not weaken one unit's gates because another unit is well documented.

## Serviced-existing: existence lane

A completed equipment-specific service, evaluation or maintenance description can prove a durable physical appliance existed. Explicit quantity can support multiple existing units even with no nameplates. Return candidate units with blank unknown identity fields, an existence-evidence pointer and `serviced-existing` basis. Actual creation of missing inventory cards requires the separately approved reconciliation policy and write plan; do not route these through strict installed-new gates or label them new installations.

A service date is not an installation date. A replaced igniter, zone-valve motor, breaker, fuse or filter is normally a repair to a parent, not another major appliance. A component may be independently tracked only when the configured business allowlist says so. Historical scheduled records with credible performed-work text remain conflict evidence for review, not silently converted to complete.

## Identity and source precedence

Use field-specific precedence rather than one universal ranking:

- Target physical nameplate controls exact model/serial over conflicting profile fields, brochures and registration transcription.
- A correctly matched completed-job worksheet or registration can provide documentary identity when no readable plate exists; report documentary provenance, not plate verification.
- Installed consumer/nameplate branding controls make. Parent corporations and warranty-program names are not automatically equipment brands.
- Exact-model manufacturer literature controls product classification/specification, but cannot establish ownership, current presence, installed fuel conversion or serial identity.
- Completed installation records establish installation timing; serial decodes usually establish manufacturing date. An attached maintenance visit establishes neither.

Preserve raw OCR and normalized comparison fields separately. Do not fill ambiguous characters using a sibling's known serial. Full distinct serials demonstrate separate units even when model and location names match. Repeated photos of one serial demonstrate one unit. A photo of an old removed unit is not a current inventory candidate without state review.

## Dedupe decision table

| Observation | Decision |
|---|---|
| Same property, exact supported full serial, compatible component | Match and enrich only supported missing/corrected fields |
| Same model, different full serials | Distinct physical units |
| Same model only, multiple units possible | Review; never auto-merge |
| Placeholder tied to exact unit/job with corroboration | Propose update rather than duplicate create |
| Same serial at another property | Scope/relocation conflict; hold attachment and creation |
| One outdoor unit plus several indoor heads | Separate according to component trackability, retaining relationship |
| Bundle quantity applied to wiring destination | Do not multiply destination appliances |
| Fractional progress-billing quantity or repeated invoice groups | Reconcile physical scope; do not sum into units |

Missing inventory access is not evidence that a record is absent. Do not resolve a duplicate by deleting one card before preserving history and obtaining explicit remediation authority.

## Age lookup

Read exact equipment detail and attached jobs. Inspect plates and documents if install date is blank. Use hvac-equipment-reference-lookup for an applicable date-code source. Report confirmed installation date, inferred manufacturing date/range and any estimated installation range separately. Model age, manufacture year and installation year are different facts. Unsupported serial patterns return unknown.

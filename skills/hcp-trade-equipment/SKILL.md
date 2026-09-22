---
name: hcp-trade-equipment
description: Use when reviewing HCP property equipment. Gate evidence, scope, writes, and exact readback.
license: MIT
version: 2.1.0
---

# HCP trade equipment

## API-first execution preference

Use the supported public API when sufficient. For UI-backed tasks otherwise, prefer a verified authorized Alpha/internal-session API over UI clicking. Use the browser for secure login/MFA/session bootstrap, visual verification and unavailable routes, not as the default data transport. Follow the [authorized internal-session workflow](references/internal-session-workflow.md) before using a protected session; it covers tool capability gaps, isolated session jars, identity readback, current CSRF/header/schema checks, exact-operation approval and ambiguity recovery. Access denial is never permission to switch surfaces. The optional `hcp-connections` helper supplies local login and identity verification; business-operation adapters remain separate.

Route a Housecall Pro equipment request to the correct evidence and permission mode. Default to read-only review. This package describes workflows, not an installed API client. Public API reads, private alpha/React reads and writes, and optional Field Intelligence reconciliation have separate capability and authorization boundaries.

## Preflight

1. Establish the tenant, exact source identifier, requested property, purpose, and approved output. Validate an HCP job identifier against the declared `job_` plus 32 hexadecimal-character format before lookup; do not repair malformed input. A display number, invoice number, estimate option, and numeric web route are different namespaces.
2. Choose `installed-new`, `serviced-existing`, `age-lookup`, or `read-only-evidence`. Record that choice before interpreting completion evidence. An age question is not authorization to create records.
3. Discover configured adapters and their tenant-scoped read/write permissions. No named helper or `equipment_*` operation is assumed available. Refresh expired private sessions through the configured secure authentication adapter; never request secrets in chat or substitute an empty public result for unavailable private inventory.
4. Start a capability/coverage ledger. Distinguish successful empty reads, failed reads, unqueried surfaces, and partially paginated results. Confirm rights to use source data; keep evidence and private identifiers out of public deliverables.
5. Read [scope and collection](references/scope-and-collection.md), then [mode gates and identity](references/mode-gates-and-identity.md). Any write also requires [guarded mutations](references/guarded-mutations.md).

## Procedure

1. Obtain the job body, direct line items and descriptions, completion evidence, notes, job attachments, customer-level supporting documents, real service address and current equipment. Gather independent reads concurrently only within the same tenant and permission scope.
2. Resolve every row to the intended customer/property. Query parameters are hints, not scope proof. Reconcile list counts and pagination before using absence as evidence.
3. Normalize physical units: identify parent appliances, independently tracked components, controls/accessories, proposed replacements, removed units, and service targets separately. Distinct serials distinguish same-model siblings; repeat images do not add units.
4. Attribute each field to its artifact. A legible target-unit plate outranks a conflicting registration for identity. An installation document may establish an install date a plate cannot. Product literature explains a model but does not prove that unit exists at a property.
5. Apply the selected mode gates. Installation completion does not make every pictured unit newly installed. Completed equipment-specific maintenance can establish an existing unit without establishing its model or install date.
6. Read and deduplicate existing property equipment, including placeholders. Propose enrichment before creation. Cross-property matches require review, not automatic reassignment or attachment.
7. Map trackable units to current configured taxonomy using [taxonomy and structured notes](references/taxonomy-and-notes.md). Apply the business trackability allowlist before the broad provider enum; an enum entry alone is not permission to track an accessory.
8. Return a dry-run plan. Execute only separately authorized mutations, with before-state checks, an idempotency strategy, sequential write/attach/readback, and explicit partial-failure reporting.
9. Deliver the receipt and unknowns. Never call an accepted request a verified result. For synthetic acceptance cases and receipt fields use [receipts and examples](references/receipts-and-examples.md).

## Stop conditions

Stop writes on ambiguous tenant/identifier, missing or placeholder service address, billing-only evidence, inaccessible inventory, incomplete dedupe coverage, contradictory physical identity, unapproved taxonomy fallback, stale before-state, missing write authority, or any failed post-write verification. Preserve read-only findings with the exact blocker. A missing model does not prohibit a read-only serviced-existing candidate; it can prohibit strict installed-new creation.

Do not run discovery POSTs or delete records to test capabilities. Never hard-delete pre-existing customer equipment. Never release a purchase order, send customer communications, change customer tags, replay production pipelines, or publish project media from an equipment review alone.

## Verification receipt

Include mode, scope proof, collection coverage, physical-unit decisions, evidence pointers, unknowns/conflicts, proposed versus executed operations, successful record-write counts, field-level readback, exact source-job relationship verification, and unresolved actions. Keep physical-unit counts separate from record-write counts. A paired-store unit can require multiple records.

## Related workflows

Dependency skill names are routing hints, not bundled capabilities: hcp-alpha-data-collection for private collection; hcp-trade-equipment-job-review for scope review; hcp-equipment-nameplate-extraction for target OCR; hcp-equipment-evidence-adjudication for conflicts; hcp-equipment-profile-reconciliation for guarded HCP/optional secondary-store plans; hvac-equipment-reference-lookup for manufacturer facts.

The legacy umbrella also covered account reports, galleries, procurement and recovery. Their retained boundaries are in [adjacent workflows](references/adjacent-workflows.md); they must not widen an equipment request's authority. Editorial choices and historical conflicts are recorded in [source decisions](references/source-decisions.md).

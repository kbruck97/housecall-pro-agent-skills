# Optional mutation handoff: never implied by review

This package does not execute HCP writes. A real configured write adapter and explicit user authorization are required. Historical alpha create/patch/attach patterns are private integration observations, not universal tools. CSRF behavior, type identifiers, create response shape, and idempotency must be verified by the installed adapter's contract; do not assume either “CSRF required” or “cookie alone sufficient.”

## Read-only plan first

The plan contains:

| Field | Requirement |
|---|---|
| `plan_alias`, `review_alias` | Link decision and evidence |
| `tenant_alias`, `property_alias` | Verified scope |
| `authorization_alias` | Specific approval and allowed operation set |
| `adapter_alias`, `contract_version` | Real configured integration binding |
| `operation` | `create`, `enrich`, `attach_existing`, or `hold` |
| `unit_alias`, `record_alias` | Exact intended target via private mapping |
| `expected_before` | Approved field projection/version for concurrency check |
| `proposed_fields` | Explicit changes only; omitted fields unchanged |
| `taxonomy_mapping` | Current valid adapter type plus semantic mapping rationale |
| `idempotency_key` | Stable opaque operation key, scoped to tenant/property/unit/operation |
| `evidence_aliases` | Unit-specific proof |
| `readback_checks` | Exact record fields, property, and real source-job linkage |
| `recovery_policy` | Bounded retry and partial-success reconciliation |

Do not put credentials or real record tokens in a distributable plan example. Do not choose a weaker taxonomy merely because a write failed. Hold the operation if the type mapping is semantically wrong or not supported. Never create/delete test equipment as capability discovery.

## Gates by operation

**Create installed-new:** exact installation proof, real service property, permitted durable class, independently supported unit identity, complete fresh live dedupe, approved field projection, and write authority. The conservative identity minimum is a supported make/model pair or a uniquely identified readable unit plate with type/role; a generic “boiler install” is not enough for this mutation gate. A physical profile may legitimately carry less identity without passing this gate.

**Create serviced-existing:** not authorized by an installed-new task. Requires explicit inventory-backfill authority, direct evidence of this durable unit at the property, distinct-unit count/role proof, policy permission for unknown identity, complete fresh dedupe, and blank original install fields unless independently documented. Never relabel it as newly installed to pass an installation gate.

**Enrich existing:** prove the record represents the same physical unit, including placeholder records. Preserve unrelated notes/history; proposed before/after changes must isolate corrections. Do not overwrite predecessor identity with replacement identity without a separately approved reconciliation plan.

**Attach existing:** verify record and source job refer to the same unit/property and that a link is actually missing. A note mentioning a job is not a linkage. Attachment is a mutation requiring approval even if the adapter claims idempotency.

**Retire/merge/relink/delete:** out of scope for routine job review. Hand off a separate evidence-backed identity plan to an authorized reconciliation workflow. “Remove candidate” means exclude it from the analysis, not delete customer equipment.

## Execution and exact verification contract

1. Immediately before an authorized write, re-read the exact target and relevant property inventory. Recompute the match; abort on drift or new duplicates.
2. Execute only the approved operation through the real adapter. Keep dependent operations sequential. Record operation key, attempt status, and target alias without logging request secrets.
3. If a successful create response lacks a usable record identity, reconcile through a scoped exact-key read before retrying. A timeout or missing ID is ambiguous success, not proof that nothing happened. Never blind-retry create.
4. Read the exact equipment detail and actual job relationship list after each operation. Verify property, type, approved identity/date fields, and exact source job linkage. A 200 response, echoed payload, or notes text is insufficient.
5. On partial failure, retain verified steps and unresolved steps separately. Re-read current state before resuming. Do not undo by deleting pre-existing equipment or declaring the entire plan complete.
6. Receipt each operation as `planned`, `attempted_unverified`, `verified`, `failed`, or `held`. Include expected versus observed comparison, linkage proof, and unresolved effects. Aggregate attempted count and verified count separately.

A mutation receipt is complete only when every approved operation is accounted for and all claimed effects are read back. The editorial validation receipt bundled with these drafts is not a live mutation receipt.

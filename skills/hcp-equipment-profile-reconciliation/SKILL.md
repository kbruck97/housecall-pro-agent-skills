---
name: hcp-equipment-profile-reconciliation
description: Use when reconciling HCP equipment profiles. Plan physical identity, guard writes, and verify exact readback; Field Intelligence is optional.
license: MIT
version: 1.0.0
---

# HCP equipment profile reconciliation

Reconcile physical units, not merely similar database rows. Default to a read-only inventory and proposed change plan. This package supplies procedures and data contracts, not an HCP client or a deployed transaction server.

## Preflight

1. Establish the authorized tenant, customer, property scope, evidence cutoff, and requested mode: `installed-new` or `serviced-existing`. A profile may contain both, but classify each unit separately. Obtain explicit approval before any mutation, including linking, merging, retiring, or correcting names.
2. Validate source identifiers without repairing them. Bind the service property independently of the billing address. Stop for a placeholder property, ambiguous customer, or unresolved property match. Keep HCP and optional Field Intelligence address namespaces separate.
3. Inspect the actual adapter's capabilities, authentication isolation, schema, pagination, readback support, and failure semantics. Use documented public reads where supported. Private alpha access is opt-in, unsupported, tenant-specific, and never implied by public access. Field Intelligence is a separate optional adapter. A missing adapter leaves a read-only plan, not an invitation to invent a tool.
4. Gather complete authorized current equipment inventories and source-job evidence. A failed or incomplete read is not an empty inventory. Check every row's scope even when a server accepted a filter. Record pagination coverage and excluded properties. Never broaden collection beyond authorized scope merely to work around a filter.
5. Agree on canonical type/name policy, unknown-field representation, dry-run approval, and concurrency guard. Keep restricted source material separate from the sanitized plan.

Consult [adapter boundaries](references/adapter-boundaries.md) before binding any runtime, and [plan and receipt contracts](references/plan-and-receipt-contracts.md) before producing artifacts.

## Procedure

1. **Adjudicate physical units.** Use exact unit evidence, serial when reliable, model, role, location, service history, and existing linkage together. Same model or broad type does not establish identity. A linked HCP card and FI row represent one unit only when the evidence is compatible. Source conflicts do not automatically mean a second unit.
2. **Separate work semantics.** `installed-new` requires evidence of actual installation, not a proposal or completion status alone, and sufficient identity under the install-review policy. `serviced-existing` permits a durable unit established by equipment-specific completed maintenance/evaluation and explicit quantity even when make/model/serial are absent. Leave installation date blank; service date is not installation date. Generic service, complaint-only notes, and unquantified plural wording do not establish a unit count.
3. **Apply component boundaries.** Filter cartridges, minor repairs, and replacement consumables normally describe service to a durable parent. Create no component asset unless taxonomy and evidence establish an independently trackable durable unit. Never inherit predecessor attributes onto a replacement.
4. **Build the whole-property plan.** Assign one physical-unit label per unit. Claim each HCP card and FI row separately against that label; explicitly leave unrelated units unchanged with a reason. Cover existing property units even if the job touched only one. Customer-wide reads support cross-property deduplication, not permission to move records.
5. **Resolve identity separately from fields.** A known linked pair can remain one unit while its model is disputed. Preserve populated conflicting fields unless stronger primary evidence settles them. Normalize a coarse type only when exactly one class is supported. Names reflect supported role/location; use a neutral unit label rather than inventing a room.
6. **Approve the exact plan.** Include per-operation evidence, expected current state, changed fields, target store, dependencies, and unresolved items. Merges need same-unit proof and explicit survivor/history disposition; retirement needs evidence the unit is no longer active. Neither follows merely from a duplicate-looking name. No discovery probe creates or delete-and-recreate shortcuts.
7. **Execute guarded operations sequentially.** Recheck current state immediately before each dependent write. Stop affected writes on stale state, identity refusal, or uncertain outcome. Never retry through a counterpart record to evade a conflict. Capture each attempted operation, response, and readback separately.
8. **Verify and remediate.** Read the exact written records, their links and source-job associations, then rerun property invariants. Check names/types, property scope, unique physical identity, no orphaned links, all plan claims, and unchanged unrelated units. Repair only evidence-supported issues within approval. If a field is silently dropped, mark it unpersisted; preserve supported evidence in notes only if separately permitted.
9. **Close from observed state.** Re-fetch the inventory after the last remediation. Derive physical-unit totals from plan labels and write totals from the operation ledger. In paired-store mode, one unit can require two creates. Repeated successful updates count as separate writes, not separate units. Refused attempts are not successes. Report unresolved issues even when an adapter allows administrative close.

## Stop conditions

Stop mutations for missing authorization, unknown service property, incomplete inventory, unresolved identity, cross-tenant session mismatch, unavailable readback, changed preconditions, or paired-store partial failure. A unit-specific field dispute may leave other independently approved units processable; a tenant/scope failure stops the entire transaction. Exhausted retries or a close refusal end as blocked/partial, not fabricated success. Do not loop indefinitely to obtain a clean close.

## Verification receipt and output

Return mode, coverage, per-unit decisions, successful write counts, verified postconditions, unchanged/unresolved fields, and smallest evidence needed next. Distinguish `planned`, `applied-unverified`, `partial`, `verified`, and `blocked`. No-write work can be a verified audit but must not claim an applied reconciliation. The optional private adapter may require an exact machine response; that is its negotiated contract, not a universal output rule.

Use opaque aliases in shared reports. Do not include customer identity, addresses, raw record identifiers, access details, signed media links, or authentication material. Dependency skills hcp-trade-equipment-job-review, hcp-equipment-evidence-adjudication, hcp-equipment-nameplate-extraction, and hcp-alpha-data-collection are companion procedures, not automatically available runtime capabilities.

## References

- [Plan and receipt contracts](references/plan-and-receipt-contracts.md)
- [Adapter boundaries and partial failure recovery](references/adapter-boundaries.md)
- [Synthetic acceptance cases](references/synthetic-acceptance-cases.md)
- [Editorial source decisions](references/source-decisions.md)

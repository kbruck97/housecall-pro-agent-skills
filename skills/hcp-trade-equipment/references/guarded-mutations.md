# Guarded mutation and recovery contract

This reference is an opt-in private-adapter design, not a declaration of current endpoint support. GET-only reviews must not execute these operations.

## Plan before write

A plan must identify tenant/property, source jobs, physical-unit key, target record, operation, evidence for every changed field, expected before-state/version, desired after-state, taxonomy mapping, idempotency key, relationship changes and verification reads. Keep sensitive locators in a restricted plan. Approval must cover the exact operations, not merely the collection task.

Use compare-before-write or adapter-provided optimistic concurrency. If the record changed after analysis, re-read and replan. Sequentialize dependent operations and same-property work. Never force a stale match from an earlier model response.

## Historical private operation shapes

These sanitized observed-internal templates are non-executable historical evidence. Explicit opt-in and current operation/schema/security verification, tenant/property checks and exact-operation authorization are required before a separately implemented adapter may use any shape.

| Operation | Observed route template | Important fields and conditions |
|---|---|---|
| Create | `POST /alpha/equipment` | `address_uuid`, `equipment_type_id`, `name`; optional evidence-supported `make`, `model`, `serial_number`, `install_date`, `notes` |
| Enrich | `PATCH /alpha/equipment/{equipment}` | Preserve unrelated fields; include only supported intended changes and required canonical fields |
| Attach | `POST /alpha/equipment/{equipment}/attach` | `job_id`; verify membership and relationship separately |
| Read detail | `GET /alpha/equipment/{equipment}` | Compare persisted fields, type and property |
| Read links | `GET /alpha/equipment/{equipment}/service_requests` | Confirm exact job, customer/property relationship and source scope |
| Hard delete | `DELETE /alpha/equipment/{equipment}` | Not normal reconciliation; exceptional separately authorized cleanup only |

Do not assume session cookies alone always satisfy write security, that CSRF is unnecessary, or that a private route is stable. The configured adapter handles current security requirements without exposing secrets. Create-time association fields may be ignored; explicit attachment plus readback is required when the adapter uses separate associations.

The category field `equipment_type` historically could silently remap to a generic category. Use the configured validated identifier field, then compare actual persisted type. Never choose a known-wrong class simply because it writes successfully. Do not typo-repair or reuse historical taxonomy IDs. A taxonomy read proves available labels, not successful writes; unsupported writes require review or explicitly authorized sandbox testing, not live probe-created customer cards.

## State machine

`planned -> approved -> before_state_confirmed -> record_written -> record_readback_verified -> relationship_verified -> complete`

Any branch may terminate as `blocked`, `stale_plan`, or `partial_failure`. Count a field as persisted only after exact detail readback. Record both requested and observed values when the adapter silently drops fields. Preserving an unsupported specification in notes may be acceptable under the plan, but is not equivalent to populating a first-class field.

Do not blindly retry a timed-out create: first search current scoped state and idempotency evidence to determine whether it succeeded. Attachment idempotency is an adapter capability to verify, not a universal guarantee. If create succeeds and attach fails, report an unlinked record and retry only the missing step after fresh checks. Do not create again.

Deletion is destructive, not archiving. A record name that looks like a probe is insufficient deletion authority. If explicit cleanup is approved, prove exact creation ownership from the operation ledger and that the record gained no unrelated history, then verify deletion. Never delete pre-existing equipment to simplify dedupe.

## Interrupted pipeline recovery

Separate failed model requests from unique business jobs: one job may have analysis and several matching requests. A recovered model response does not resume its abandoned caller or perform CRM writes. Verify provider recovery with one harmless canary; then rerun only the exact authorized jobs through the configured real pipeline, sequentially per customer/property. Obtain fresh inventory and matching decisions. Keep request recovery, business replay and downstream completion as separate ledger states.

Require detail and exact source-job-link readback for every affected record. Account for created, updated, existing, folded, review and failed outcomes. Do not reset webhook ledgers, release locks, or replay historical production events under an equipment-review authorization. Those operations require their own runbook and permission.

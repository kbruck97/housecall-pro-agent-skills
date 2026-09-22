# Adapter contract and verification gates

This package is operational knowledge, not an installed HCP SDK. Implementations must supply an explicit adapter and prove its behavior offline before tenant access. [Foundations](../skills/hcp-foundations/SKILL.md) governs authentication and authority; [capabilities](capabilities.json) contains official source URLs and evidence levels.

## Transport preference

Use the supported public API when sufficient. For UI-backed tasks otherwise, prefer a verified authorized Alpha/internal-session API over UI clicking; reserve the browser for secure login/MFA/session bootstrap, visual verification and unavailable routes. Follow the [authorized internal-session workflow](internal-session-workflow.md), including runtime capability, identity readback, current CSRF/header/schema verification and no access-denial bypass. This preference does not install an adapter or expand authorization.

## Required request boundary

Accept typed inputs: `tenant_ref`, `company_ref`, `surface`, `operation`, canonical resource references, validated parameters, collection budget, and separately scoped approval reference for mutations. Resolve secrets from a protected provider. Never accept arbitrary model-provided URLs, credentials or cross-tenant selectors. Pin trusted origin, allowed HTTP method/path, exact parameter serializer and response envelope for each operation.

Use separate public-key, public-OAuth, internal-session, FI and external-download clients. Public API keys use Token; partner OAuth uses Bearer. Internal `/alpha` access is never silently substituted for a failed public read. FI is an integration-specific projection, not an authoritative HCP endpoint. Third-party downloads must have no HCP headers and must validate redirects.

A ledger entry with `expanded-sidebar`, `overview-family`, `research-family`, `official-index-only` or unresolved method/path/body is discovery evidence, not executable permission. Resolve and version the operation-specific schema before enabling it. Do not generate routes by pluralizing operation names.

## Required result boundary

Return a typed result with:

- `surface`, `operation`, company-scope validation and resource relationship validation;
- `outcome`: success, partial, blocked, failed or ambiguous;
- requested/received page metadata, distinct row counts, expected totals, completeness reason and next checkpoint;
- fetched-at interval, source version/evidence level, missing/unexpanded fields and normalized status alongside raw status;
- sanitized HTTP status/error class and retry/reset metadata, never Authorization/Cookie or signed URL values;
- for authorized writes: local intent reference, provider receipt reference when available, exact readback result and unresolved side effects.

Do not make a network failure look like an empty successful list. A budget-limited scan is partial. A successful write response without readback is submitted, not verified. Preserve null monetary allocations as unknown and guard invoice customer_uuid array serialization explicitly. Routes require request per_page even though their response says page_size.

## Safety and local recovery

Default GET-only. Separate approvals for ordinary edits, notifications, scheduling commitments, estimate approval/decline, financial changes, bulk replacement, deletion/locks/admin settings and publication. Persist intents before submission and reconcile ambiguous results before retry. Do not claim server-supported idempotency without official operation evidence. Preserve irreversible provider acceptance even if local projection/audit fails.

A read-only key is defense in depth, not a replacement for method enforcement. A supported endpoint is not an approval. Internal and FI adapters need their own authorization, tenant isolation and provenance checks; no executable private adapters or credential/session files belong in this package. Sanitized historical observed-internal route templates are retained as non-executable design references only. Their use requires explicit opt-in, current operation/schema/security verification, tenant/property checks and exact-operation authorization.

## Offline acceptance matrix

Use synthetic fixtures and deny all network in tests. Assert:

1. Token versus Bearer selection; wrong company/origin or mixed selectors block; read-only mode rejects every non-GET.
2. page/page_size and routes page/per_page contracts; changing totals, duplicate/repeated pages, malformed metadata, empty pages, bounded interruption and complete multi-page termination.
3. 429 epoch reset parsing and bounded retry, no invented universal rate ceiling; 401/403 never return success-empty.
4. Customer scope including invoice-to-job joins and array serialization; ignored filters are detected by returned scope.
5. Unexpanded versus empty associations; completed query versus raw completion/cancellation states; approval status change not approved-at.
6. Split invoice invoiced_amount versus repeated amount; null allocation unknown; paid deposit not final payment/completion.
7. Cross-origin attachment requests and redirects strip HCP credentials; exports reject secrets, PII, signed URLs and spreadsheet formula injection.
8. Mutation timeout reconciliation, no blind retry, exact readback mismatch, provider accepted/local ledger failure and explicit notification intent.
9. Webhook exact-byte HMAC, invalid/stale signature, trusted tenant mapping, durable enqueue failure, concurrent duplicate, failed-run retry and stale event ordering.

A test pass proves only these synthetic contracts. Record tenant read-only verification, approved canary mutations and live operational readiness separately; packaging never enables them.

## Provenance and remaining gaps

The draft uses the official-documentation research snapshot associated with 2026-09-21 and sanitized reusable lessons from account/equipment evidence, procurement readiness, webhook disablement forensics and invoice reconciliation references. No customer examples, private identifiers, host paths, cookies or credentials are carried forward. Sanitized historical `/alpha/equipment` templates are retained in the equipment guarded-mutations reference as observed-internal, non-executable evidence, not current endpoint support or permission to execute. Private identifiers, tenant configuration and session implementations remain omitted.

Outstanding: per-operation payload/security schemas beyond extracted reads; exact array encoding; webhook header/encoding details; current entitlement conflict; checklists; employee-create conflict; unsupported public charge/refund, invoice-send, equipment and service-plan CRUD. Source date attribution is at snapshot level because per-page fetch timestamps were not preserved. Do not upgrade evidence levels merely because a later adapter returns 200.

---
name: hcp-webhook-recovery
description: Use when validating HCP webhooks or recovering gaps. Separate signed receipt, durable processing, reconciliation, and replay authority.
license: MIT
version: 1.2.0
---

# HCP webhooks and recovery

Read foundations (dependency skill `hcp-foundations`), [adapter contracts](references/adapters.md), and the [ledger](references/capabilities.json). This is a runbook, not a configured receiver or permission to enable delivery/replay. Official documentation establishes signed job, appointment, customer, estimate, organization-app, lead and invoice event families. It does not establish a public delivery-history or replay API, a delivery SLA, or a retry schedule.

## Receive and process safely

1. Route to a trusted tenant/signing-secret mapping. Never choose arbitrary secrets or company context from an unverified payload alone. Apply size limits and preserve exact received body bytes.
2. Validate the documented signature format over timestamp + `.` + payload using HMAC SHA256 and the signing secret. Obtain actual header names/encoding from the current official webhook schema; this research does not reproduce them. Compare in constant time. Reject invalid signatures before business processing.
3. Apply a documented local timestamp/replay policy, with bounded clock skew and secret rotation handling. These are integration controls, not claims about HCP's delivery timing. Test that JSON reserialization changes verification and is not used as the signing input.
4. Persist a verified receipt durably before acknowledging accepted work. If durable persistence fails, do not return a success acknowledgment that loses the event. Keep transport acceptance separate from workflow success.
5. Deduplicate on a provider-documented event identity where available; otherwise define an explicit local dedupe key and collision policy. Tenant belongs in every key. Atomic claims prevent concurrent duplicate processing. A failed run remains retryable, a running duplicate points to its current run, and success is recorded only after business effects reconcile.
6. Map all entry paths, including replay, through the same validated normalization. Preserve source event time and current state; do not let delayed events overwrite newer scheduling/payment/lifecycle state. Where ordering is ambiguous, re-read authoritative HCP resources and hold rather than applying guessed precedence.
7. Separate processing from customer sends, HCP writes, and FI equipment work. Keep each side effect default-off unless specifically authorized. A paid event alone cannot trigger post-job contact: final balance and current completion still matter.

## Diagnose delivery gaps read-only

Identify the last accepted real event, receipt and worker lag, receiver status/error window, ingress health, app enablement evidence, and configuration equality without printing secrets. Correlate independent timestamps; do not claim a disable actor/reason from “is_enabled=false.” An internal status adapter is an `observed-internal` supplement and may not expose actor, reason, disable time, or provider delivery history.

Compare healthy and unhealthy intervals without reusing the cause of an older outage. A test payload accepted with 200 proves transport/configuration, not processing of a real business event. Individual webhook setup is an owner/UI flow; partner OAuth setup may require HCP developer coordination. Do not invent setup or re-enable API endpoints.

## Recovery procedure

1. Freeze an incident window and distinguish missing receipts, failed worker attempts, unique business resources, and already-applied side effects. One job may produce several events and processing requests.
2. Reconcile the bounded company/resource cohort using documented public reads. Record data gaps and cache drift; a reconcile report does not itself mutate projections.
3. Obtain explicit scope approval before replay or enablement changes. Replay only identified failed/missing work through the real authorized integration pipeline, never by fabricating a signed HCP event or calling an invented vendor replay endpoint.
4. FI replay is an integration operation, not HCP replay. It needs its own tenant binding, intent/receipt ledger, schema, failed-state rules and authorization. A successful model response or HTTP receipt does not prove equipment creation, attachment, database projection, or any downstream effect.
5. Re-read current state before retries; do not force stale dedupe decisions. Preserve provider-accepted receipts even if local bookkeeping failed. Ambiguous effects require reconciliation, not blind resubmission.
6. Verify exact intended outputs at each boundary: durable receipt, completed worker, current projection, any separately authorized HCP mutation readback, and final absence of unresolved business-resource gaps. Report recovered, already-complete, failed, and held separately.

## Examples and tests

**Positive:** A verified duplicate of an in-flight event maps to the existing run; a failed run is retried only after current-state reconciliation and an approved replay scope.

**Negative:** A successful manual model replay is reported as recovered HCP equipment, or a save/test webhook is treated as a completed job. Neither proves business effects.

Offline acceptance cases: invalid signature, changed bytes, stale timestamp, wrong tenant, concurrent duplicate, failed retry, late out-of-order event, durable-write failure, provider success/local failure, and a test payload with no business identity. Live enablement and replay remain owner-gated.

For adjacent integration work, read [stateful canary boundaries](references/stateful-canary-boundaries.md); its separate authority gates remain mandatory.

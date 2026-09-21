# Adapter discovery, consent, and durable effects

This package defines semantic requirements, not executable tool names or Housecall Pro API endpoints. A deployment may combine HCP records with a separate communications, work-item, consent, or scheduling provider. No adapter is bundled or certified here.

## Commissioning contract (read-only discovery first)

1. Inspect the supplied tool catalog, operation schemas and deployment documentation; do not guess endpoints, credential locations, CLI flags, or tool names. Do not probe by creating/deleting records.
2. Record each actual binding with provider, version, supported operation, tenant authorization, input identifier format, output fields, read/write classification, permission scope, pagination, freshness guarantees, rate/error semantics and exact-target readback operation. Unknown means unavailable, not assumed support.
3. Distinguish documented public HCP capabilities from explicitly enabled private/internal integrations. Never silently fall back between providers or tenant sessions.
4. Require capabilities appropriate to the proposed action:
   - Source reads: exact customer, property and lead/estimate/invoice/job relationship; timestamps and authoritative status.
   - Conversation reads: authorized candidate journeys, inbound history, owner, pending work and outbound ledger.
   - Consent reads: current endpoint/channel/purpose permissions, DNC, wrong-number and suppression history.
   - Optional writes, each separately authorized: consent suppression, durable internal handoff, message dispatch, journey update, booking, or business-record mutation.
   - Exact receipt lookup/readback for every enabled write; idempotency and unknown-outcome reconciliation.
5. A read-only snapshot permits analysis, not outreach. Set `mode: draft` by default. Approved writes need explicit tenant, operation, target, content/parameters, approval reference and expiry. Tool availability and tenant policy do not grant authority.
6. If source reads are missing, accept a supplied snapshot only as dated evidence. Mark freshness unverified and produce a blocked/draft decision; do not infer current eligibility.

## Shared routing and privacy gates

Determine the semantic intent among deterministically authorized candidate journeys. A phone is an endpoint, not a journey identity. Do not let board priority hide a complaint, hazard, opt-out, wrong number or unrelated service request. Uncertain tenant/party/property/journey linkage blocks record disclosure and mutation. Do not repair malformed identifiers; validate against the actual adapter contract and preserve the original for operator correction.

Read consent before any ordinary outbound message and recheck immediately before dispatch. A known phone or past purchase is not consent. Unknown permissions fail closed for automated outreach. A reply permits only what the configured channel/purpose policy authorizes, not a new campaign. Respect local quiet hours and tenant timezone; unknown timezone blocks scheduled outreach.

STOP/opt-out: suppress ordinary automation immediately in this decision, and use the authorized consent actuator to persist suppression when enabled. Read back the exact endpoint/channel scope. If persistence is unavailable or fails, report `suppression_pending` and an urgent internal remediation need; never claim global DNC was saved. Do not switch channels to evade the request.

Wrong number: first-class privacy/consent correction, not a demand for another keyword. Suppress future outreach, reveal no intended-recipient or record details, and draft at most one neutral apology only when policy allows. Any permitted acknowledgment is subject to authorization and provider consent rules; silence may be required.

Mixed STOP and hazard: retain both intents. Persist suppression and create an internal safety escalation independently; success in one is not success in the other. Do not let consent suppression discard risk evidence. Do not use a keyword-to-physical-action table or continue remote troubleshooting. Keep any immediate safety guidance situational and within competence; do not imply service dispatch.

Disputes, repeated complaints, communication breakdown, property damage, legal/review threats and safety concerns pause ordinary follow-up. Route to the appropriate human owner and send at most one factual acknowledgment if allowed. New urgent information can supplement internal escalation; do not resume marketing while a human owns the case without an explicit release.

## Durable receipt and claim gate

A draft note, model output, queued plan, local log or successful HTTP status alone is not a handoff. A durable handoff needs a stored work-item/escalation identifier, correct tenant and target, issue summary, queue/owner and readback. Only then may copy say “I've sent this to the office to review.” A queue receipt does not prove a specific person accepted the work or will call by a deadline.

Without a verified handoff, say “I don't have a verified answer to that” and offer only the tenant's verified contact option, if one exists. Do not say “soon,” “shortly,” “right away,” “give us a day or two,” or “the office will confirm” without an independently evidenced commitment. A selected appointment window is a preference; a hold requires a hold receipt, a booking requires a booking receipt and exact booking readback.

Before any enabled write: refresh source, consent and ownership; ensure approval still applies; resolve an existing semantic action key; apply documented concurrency control. Keys must bind tenant + journey/source entity + action/purpose + policy step, not merely a changing event timestamp or phone. A repeated webhook is not a new journey or additional touch. Never reset attempt counts to bypass a cap.

After a write: read the exact target from the authoritative adapter; compare scope, content/status and relationships. Keep `requested`, `accepted`, `persisted`, `delivered`, and `verified` distinct. Provider acceptance is not delivery. On timeout/unknown outcome, query by the original idempotency key/receipt before retry; if no safe lookup exists, stop for reconciliation. Partial success must remain visible (e.g., handoff persisted, outbound failed); do not repeat successful operations.

## Cadence is configuration, never authority

No automatic schedule is installed by this package. Require an approved policy version, eligible anchor, timezone, quiet hours, maximum touches, spacing semantics, retry rules and stop conditions. Distinguish offsets from the original anchor versus delays after a prior touch. Historical timing is migration context only. Preserve actual touch history when policy changes. Human replies, DNC, wrong-number, hazards, handoff ownership or a changed source state supersede “due.” Missing/conflicting cadence means draft-only and operator review.

## Failure dispositions

| Failure | Required disposition |
|---|---|
| No read adapter / stale snapshot | Draft with freshness gap; no current-state claim |
| Tenant or party ambiguity | Block disclosure and action; request authorized mapping |
| Missing consent / sender / approval | Block outbound; do not fabricate a tool |
| Handoff unavailable | Handoff needed, not completed; no callback promise |
| Suppression write failed | Keep local suppression and flag durable remediation |
| Write timeout / ambiguous receipt | Reconcile before retry; do not report success |
| Readback mismatch / partial write | Pause further effects; retain all receipts and escalate |
| Concurrent owner / duplicate journey | Reconcile canonical owner before any touch |

Store minimum necessary customer data in authorized systems only. Package fixtures contain invented labels, never real phones, addresses, record IDs, tokens or payment URLs.

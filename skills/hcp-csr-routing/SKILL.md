---
name: hcp-csr-routing
description: Use when routing field-service customer turns. Preserve consent, journey ownership and evidence-backed actions.
license: MIT
version: 1.0.0
---

# HCP CSR routing

Use for front-office SMS/voice, mixed-intent conversations and operator routing audits. This is the semantic router, not a sender or a universal HCP integration. Default to read-only classification and draft copy. Follow [adapter and receipt gates](references/adapter-contract.md), [tenant overlays](references/tenant-overlays.md), and [composition audits](references/composition-audit.md).

## Procedure

1. Separate customer turns from operator requests. “What is due?” is a read-only scanner request; “what has the agent done?” is an operations audit, not a customer message.
2. Discover the runtime's actual read capabilities and trusted tenant/party binding. Read the current delivered thread, domain state and authorized candidate journeys. Do not equate newest board row or shared phone with ownership.
3. Detect opt-out, wrong number, concrete hazards and high-risk complaints before selecting an ordinary lane. Preserve both suppression and internal safety actions for mixed messages.
4. Select the semantic journey from authorized candidates. If ambiguous, ask one minimal clarification; never invent a journey or transfer tenant scope. Handle unrelated support even while an estimate/invoice journey owns the endpoint.
5. Choose a route below, retaining secondary intents and risk flags. An estimate decline after choosing another provider is a no-pressure close, not automatically an emergency. A complaint about conduct during that switch may require escalation.
6. Read the chosen journey's authoritative facts, apply its policy, then return a draft/proposed action. No prices, availability, diagnosis, payment links, assignments or successful actions from memory.
7. If execution is separately authorized, deterministic adapters own side effects, idempotency and sends. Read back receipts and check final copy against them before sending. Missing handoff capability means blocked handoff—not an invented promise.

## Routing map

| Semantic intent | Owner | Important boundary |
|---|---|---|
| New service, pricing or consultation | lead follow-up | A lead is not a booking |
| Existing estimate question, acceptance, revision, decline | estimate follow-up | Interest is not authoritative acceptance/conversion |
| Balance, payment link, claimed payment, plan, dispute | invoice follow-up | Customer payment claim is not paid state |
| Existing-job help, warranty, reschedule, cancellation | customer service | Request is not completed mutation |
| Post-payment satisfaction | happy calls | Service recovery overrides promotional asks |
| Due/pending/overdue inquiry | follow-up scanner | Read-only; no enrollment, replay or send |
| Dormant preventive maintenance | maintenance reengagement | Verified lifecycle shortlist, not a happy call |
| Concrete safety, damage, legal/billing conflict, repeated complaint | human escalation | Pause ordinary outreach, preserve internal safety action |
| Choosing verified appointment availability | scheduling | Exact fresh slot plus final booking receipt |

Keep universal communication ledger, follow-up journey queue, lead intake and operations cases distinct. Link their receipts; do not collapse every state into a single “contacted” field.

## Customer delivery

One short response and at most one question. Mirror the concrete service word without inferring diagnosis. No internal system/tool labels in customer copy; this is not a mandate to lie about automation when asked—follow applicable disclosure requirements honestly. SMS does not need spelling requests, phone-style readbacks or “stay on the line.” Use a name sparingly and vary repetitive openers. Voice may use a brief lookup bridge only when work is actually underway; silence for opt-out remains intentional, not a failure to acknowledge.

## Return

Use the evidence envelope plus `intent_label`, `secondary_intents`, `selected_journey`, `missing_fields`, `proposed_action`, `must_handoff`, and exact `customer_copy` or null. Distinguish generated copy from sent copy. Operator analysis should answer directly with evidence and blockers, not customer-script output.

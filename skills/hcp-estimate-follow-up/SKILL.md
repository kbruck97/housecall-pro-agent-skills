---
name: hcp-estimate-follow-up
description: "Use when an HCP estimate needs follow-up. Draft bounded nudges and classify acceptance, questions, revisions, and declines with receipt-gated handoffs."
license: MIT
version: 1.0.0
---

# HCP estimate follow-up

Follow an issued estimate without pressure, duplicate conversion journeys or unsupported sales promises. Handle willingness to proceed, source-confirmed acceptance, scheduling, questions, price objections, revision requests and declines. **Default is read-only analysis and unsent drafts.** No HCP/messaging adapter is bundled.

Read [adapter and safety contract](references/adapter-and-safety-contract.md) before any action and use [evidence contract](references/evidence-contract.md) for every decision. Review [synthetic cases and migration decisions](references/cases-and-migration.md) for the legacy timing conflicts this package deliberately does not inherit.

## Entry and configuration

For an ordinary nudge, verify: estimate exists, correct tenant/customer/property and selected option/version are known, sent/issued evidence exists, and estimate is not accepted, declined, converted, void/canceled or otherwise ineligible under tenant policy. An event labeled `estimate.sent` nominates a candidate; it does not prove current state. Inbound questions on closed estimates can still be routed without reopening a sales cadence.

Configure company label, authorized channels/endpoints, timezone, quiet hours, approved cadence with anchor semantics and cap, estimator/office queue, pricing authority and verified contact option. Missing cadence or conflicting configuration blocks automated nudges, not read-only classification. Consent, freshness, ownership and durable receipts override all old timing examples.

## Procedure

1. **Read current source and relationships.** Capture estimate status, selected option/version, sent time, customer/property, accepted/declined flags, conversion/job links and relevant scope. Preserve exact source identifiers; verify formats against the discovered contract. Partial lists are not proof that no converted job exists.
2. **Resolve the conversation.** Select among authorized journeys based on the customer's actual intent. Check prior replies, touches, owner and pending handoffs. A converted estimate must link/transition to its existing job workflow, not create another lead or cadence. Coordinate suppression/closure of the old journey through an approved adapter; draft-only runs merely propose it.
3. **Apply shared safety/consent gates.** Wrong-number, STOP, disputes, hazards, repeated complaints and human ownership interrupt sales follow-up. Do not answer a billing complaint with another estimate nudge.
4. **Classify reply precisely.** Use the branch table below. Distinguish conversational interest from contractual/source acceptance; do not update HCP acceptance or convert/create a job from casual text without a separately authorized supported action.
5. **For a due no-reply candidate, evaluate configured cadence.** Reconcile actual outbound history, including other journey rows, against the policy cap. A duplicate event or new policy version does not reset the count. Respect timezone/quiet hours and current eligibility immediately before an approved send. Without a schedule, produce only a proposed first nudge for review.
6. **Prepare an action plan and exact draft.** Identify the source of every answer or commercial promise. Revision/discount requests are internal review requests, never promised revisions or delivery dates. An approved handoff needs a durable receipt and readback before the draft says it was sent.
7. **Execute only separately approved effects.** Re-read state before send/update/conversion/booking. Apply documented idempotency and read back the exact changed target. If the estimate converted while waiting, suppress the stale nudge. If write outcome is unknown, reconcile before retry.
8. **Close or pause correctly.** A verified decline or conversion stops ordinary estimate outreach. Final no-response closes the automated journey per approved policy, not the estimate as declined in HCP. Human questions/revisions pause nudges until explicitly released. Preserve evidence and next owner.

## Reply decisions

| Intent | Decision and constraints |
|---|---|
| Wants to proceed / schedule | Record `acceptance_interest`; check current estimate/option, then scheduling or office handoff. Only source evidence permits `source_accepted`; never invent times. |
| Question answered by current estimate | Answer briefly with source field/reference; do not enlarge scope or warranty. |
| Unknown technical/commercial question | Handoff needed; no unverified callback-time claim. |
| Price objection / revision request | Capture requested change and send for approval if enabled. No negotiation, discount, financing offer or promised revised estimate without approval. |
| Declines | Thank them without pressure; stop nudges. A single optional reason question is allowed only if consent/policy permits and no further-contact refusal exists; never make it a condition of closure. |
| No response | Use bounded tenant policy; after cap, propose closeout or internal action, never indefinite texts. |
| Converted to job | Link canonical job journey and stop estimate nudges; do not create a duplicate lead/job. |

## Journey-specific evidence

```yaml
estimate:
  estimate_ref: <authorized source reference>
  option_ref: null
  version_ref: null
  source_status: null
  sent_at: null
  conversion_job_ref: null
  reply_class: <acceptance_interest|question|price_objection|revision|decline|no_reply|other>
  acceptance_basis: <customer_interest|source_verified|null>
  requested_revision: null
  approved_offer_ref: null
  answer_evidence_refs: []
  proposed_contact_status: <active_conversation|waiting|escalate|done>
  proposed_outcome: <interested|accepted_verified|declined|converted|no_response|question|revision_needed>
  closure_basis_ref: null
```

Use `accepted_verified` only for authoritative source acceptance, not a draft sentiment classification. State mapping is adapter-specific, not a universal HCP enum.

## Safe draft patterns

Eligible nudge: “Hi {first_name}, this is {company_name} checking in on your estimate. Do you have any questions?”

Revision without a receipt: “That change would need review; I can't confirm revised pricing here.”

With verified handoff: “I've sent your question to the office to review.” This does not promise a new price, appointment or response deadline.

Read [public data operations](references/public-data-operations.md) for documented endpoints and state boundaries.

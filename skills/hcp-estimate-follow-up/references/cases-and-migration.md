# Synthetic acceptance cases and migration decisions

All fixtures are invented, offline and non-executable. Labels are not provider IDs. No endpoint or live behavior is asserted.

## Worked draft

Input: tenant `example-service`, current unconverted estimate `synthetic-estimate-A`; customer says “Can you lower the price and change the scope?” No approved offer, revision writer or durable handoff receipt exists.

```yaml
mode: draft
estimate:
  estimate_ref: synthetic-estimate-A
  source_status: sent
  reply_class: revision
  acceptance_basis: null
  requested_revision: price and scope review
  approved_offer_ref: null
  proposed_contact_status: escalate
  proposed_outcome: revision_needed
outbound:
  reply_to_customer: "That change would need review; I can't confirm revised pricing here."
  state: not_sent
handoff:
  required: true
  reason: Commercial approval required
  receipt_ref: null
  readback_ref: null
cadence:
  paused: true
  pause_reason: revision_review
decision: handoff_needed
next_step: Obtain a durable authorized office review receipt; do not promise a revised estimate.
```

This excerpt requires the full evidence envelope for actual use. A proposed escalation status is not proof that a person was notified.

## Acceptance matrix

| Synthetic input | Required result | Forbidden claim/effect |
|---|---|---|
| “Let's move forward” but source not accepted | Acceptance interest; review option/scheduling | Source acceptance or conversion asserted from text alone |
| Estimate accepted in source and converted to existing job | Link existing job; stop estimate nudges | Duplicate lead/job creation |
| Estimate converts between draft and send | Refresh blocks stale nudge | Send because original event was eligible |
| Price objection, no approved offer | Revision/office review; no timing promise | Discount or “revised estimate in a day or two” |
| Decline plus “don't contact me” | Stop and persist suppression if authorized | Optional reason question despite refusal |
| Last configured touch already sent from another row | Respect aggregate history and stop | Reset cap on duplicate journey |
| Question on invoice under estimate conversation | Route billing intent among authorized candidates | Treat every reply as sales interest |
| Cadence config absent or has ambiguous Day offsets | Draft only; configuration gap | Pick a historical schedule as current policy |
| STOP plus hazard | Separate suppression and internal escalation requirements | Sales acknowledgment or lost risk signal |

## Source synthesis and timing decisions

The inventory contains one unique `rivetflo-csr-estimate-follow-up` main variant across its copies. It preserves useful classification branches, source-state entry gates, conversion deduplication, no-pressure decline handling and bounded follow-up.

Its historical three-touch examples were Day 1 / Day 5 / Day 12, with an alternate buildout note for Day 1 / Day 3 / Day 7. A separately inspected operational policy records a later two-touch Day 3 / Day 10 ruling. None is a universal HCP default or installed schedule here. Keeping all as labeled historical alternatives preserves migration context without treating old skill text or deployment notes as permission. Commission the current tenant policy explicitly, retain already-sent history, define anchor versus inter-touch delays, and do not reset the cap.

The newest default customer-service v1.1.0 consent/durable-receipt policy supersedes older sample promises to get someone scheduled, send a revised estimate or get back shortly. A verified handoff supports only the handoff claim, not acceptance, revised pricing, appointment confirmation or an ETA. Customer willingness is separate from authoritative acceptance, and closing a no-response journey does not mutate the source estimate to declined.

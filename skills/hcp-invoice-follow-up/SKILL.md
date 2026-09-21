---
name: hcp-invoice-follow-up
description: "Use when an HCP invoice is unpaid or gets a billing reply. Draft balance-verified follow-up, distinguish payment claims, and gate links and escalation."
license: MIT
version: 1.0.0
---

# HCP invoice follow-up

Handle open balances, payment-link requests, claimed payment, billing questions, disputes and payment-plan requests accurately and conservatively. **Default: read-only analysis and unsent drafts.** This is not authorization to collect money, charge cards, alter invoices, settle disputes, refund payments or arrange financing.

Read [adapter and safety contract](references/adapter-and-safety-contract.md) for capability discovery, consent and durable receipts. Use [evidence contract](references/evidence-contract.md) plus the fields below, and [synthetic cases and migration decisions](references/cases-and-migration.md) for acceptance review.

## Entry and tenant configuration

An ordinary reminder requires current authoritative balance greater than zero, correct tenant/invoice/customer or authorized bill-to party, a noncanceled invoice/job, an eligible due state under approved policy and an authorized contact channel. An invoice-sent or job-completed event only creates a candidate; do not call a positive balance overdue without verified due-date/terms evidence. A current-state overdue scan can also nominate a candidate, subject to the same gates.

Configure company label, bill-to identity policy, currency/amount representation, timezone, quiet hours, reminder cadence and cap, billing queue, approved payment-link origin policy and verified contact option. Do not assume USD or format a balance from an unknown unit. Preserve decimal/minor-unit semantics from the contract and use deterministic calculation tools for arithmetic, never mental math. If any money field is missing or contradictory, withhold the amount and hand off.

## Procedure

1. **Resolve exact billing scope.** Read invoice/job status, balance, currency, amount units, due date/terms, recent payments/credits and source update time. Identify the authorized recipient, which may be bill-to rather than the service occupant. A phone match or shared household does not authorize invoice disclosure.
2. **Check conversation and source freshness.** Read replies, owner, touch history, disputes, payment verification work and duplicate journeys. Confirm current balance again immediately before any approved reminder. A zero balance stops collections; canceled or unclear records require review rather than another nudge.
3. **Apply cross-lane safety and consent.** Wrong-number and STOP suppress outreach without revealing balance or intended-recipient facts. Mixed hazard/STOP preserves internal escalation. Billing disputes and angry/repeated complaints pause all routine payment nudges until human release.
4. **Classify the customer's words in context.** “I paid” is a claim requiring verification. “I haven't paid yet” is not a payment claim; “I'll pay Friday” is intent, not a posted payment or approved extension. Keep claim, promise, pending payment and source-confirmed balance separate.
5. **Use the relevant branch below.** Answer factual questions only from current scoped source evidence. Never defend charges, argue, threaten, imply legal consequences or invent fees/discounts/payment terms.
6. **Evaluate bounded cadence for no-reply cases.** Require the configured anchor/due rule, offset interpretation, cap and tenant local send window. Preserve actual attempts; after the cap, stop automated nudges and prepare owner/billing escalation. Missing policy means no automatic next touch.
7. **Prepare evidence-backed effects.** Only an enabled approved adapter may send a message/link, persist suppression, create a billing work item or update a journey. No payment capture, refund, invoice adjustment or payment-plan write is in scope. Durable receipts and exact readback control what copy may claim.
8. **Verify and reconcile.** Read back each authorized effect. On ambiguous send outcome or mismatched receipt, stop and reconcile before retry. Do not close a balance or launch post-payment satisfaction outreach solely because a message was sent, customer claimed payment, or a local workflow says done.

## Reply branches

| Reply/state | Handling |
|---|---|
| Says paid | Record `payment_claimed`, pause routine nudges pending verification, and check current source. Never mark paid from text or argue. Handoff if pending/mismatched. |
| Source shows zero balance | Stop invoice follow-up; capture exact balance read evidence. Zero due can arise from credits/voids, so do not label “paid” without payment evidence. Post-payment workflows require separate eligibility review. |
| Partial or pending payment | Use authoritative remaining balance and payment status; do not subtract a claimed payment or treat authorization/pending as settlement. |
| Wants payment link | Retrieve only from trusted scoped source/API. Verify tenant/invoice association, allowed origin, intended recipient and expiry where supported. Do not construct, shorten, guess or reuse another invoice's link. Unverifiable link means no send and billing review. |
| Dispute / payment plan / charge concern | Pause automation and prepare billing handoff; capture the issue without accepting disputed facts as proven. Do not agree to a plan or waive a charge. |
| Simple factual question | Answer only with exact source evidence; otherwise handoff needed. |
| Final no response | Stop reminders and prepare owner escalation; a failed handoff remains pending, not successfully escalated. |

Do not request card numbers, CVC, credentials or one-time codes in chat. Payment entry belongs in the trusted payment provider's authorized flow. Keep signed/token-bearing payment URLs out of general evidence logs; store a restricted reference and validation result.

## Journey-specific evidence

```yaml
invoice:
  invoice_ref: <authorized source reference>
  job_ref: null
  bill_to_ref: null
  source_status: null
  balance_value: null
  balance_units: <minor_units|decimal_currency|unknown>
  currency: null
  due_at: null
  overdue_basis_ref: null
  payment_reply_class: <claimed_paid|not_paid|intent_to_pay|link_request|dispute|plan_request|question|no_reply>
  payment_verification: <not_checked|pending|partial|zero_balance|paid_verified|unresolved>
  balance_read_ref: null
  payment_read_ref: null
  trusted_link_ref: null
  link_validation: <not_requested|verified|blocked|unknown>
  proposed_outcome: <waiting|payment_claimed|link_requested|billing_escalation|balance_zero|no_response>
```

## Safe draft patterns

Verified open balance and authorized party: “Hi {first_name}, this is {company_name}. Our records show a remaining balance of {formatted_balance}. Reply here with questions.” Include an invoice label only if verified and appropriate to the channel.

Claimed payment with verification incomplete: “Thanks for letting us know. I don't yet have confirmation of the payment.” Do not say it was noted in the account unless a note write is verified.

Link unavailable: “I don't have a verified payment link to share.” Add only a verified contact option or receipt-backed billing handoff; do not promise a link shortly.

Read [public data operations](references/public-data-operations.md) for documented endpoints and state boundaries.

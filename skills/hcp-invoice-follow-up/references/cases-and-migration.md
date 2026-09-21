# Synthetic acceptance cases and migration decisions

All labels are invented and non-executable. These fixtures contain no payment URLs, real record identifiers, customer details or live financial data.

## Worked draft

Input: tenant `example-service`, authorized invoice `synthetic-invoice-A`; customer says “I paid yesterday.” Current payment read is unavailable, and no handoff has been persisted.

```yaml
mode: draft
invoice:
  invoice_ref: synthetic-invoice-A
  balance_value: null
  balance_units: unknown
  currency: null
  payment_reply_class: claimed_paid
  payment_verification: unresolved
  balance_read_ref: null
  payment_read_ref: null
  proposed_outcome: payment_claimed
outbound:
  reply_to_customer: "Thanks for letting us know. I don't yet have confirmation of the payment."
  state: not_sent
handoff:
  required: true
  reason: Verify claimed payment in the authoritative billing source
  receipt_ref: null
cadence:
  paused: true
  pause_reason: payment_verification
decision: handoff_needed
unknowns: [current_balance, posted_payment]
next_step: Obtain current source payment evidence or a verified billing handoff.
```

Complete the common evidence envelope before operational use. Nulls express unavailable evidence, not zero balance.

## Acceptance matrix

| Synthetic input | Required result | Forbidden claim/effect |
|---|---|---|
| “I haven't paid yet” | `not_paid`, current source determines eligibility | Misclassify as claimed paid |
| “I'll pay Friday” | Intent, not settlement or approved plan | Mark paid or agree to extension |
| Customer says paid, source still open | Pause for verification; preserve disagreement | Close invoice based on text or argue |
| Source shows pending payment | Pending; verify settlement/current balance | Treat pending authorization as paid |
| Source shows zero due from credit | Stop collection; `zero_balance` | Assert actual payment without payment evidence |
| Open balance but due date absent | No “overdue” assertion | Assume all unpaid invoices are late |
| Payment link is from wrong invoice/tenant | Block link and disclose nothing | Send based on a familiar-looking domain |
| Missing link adapter | Billing handoff needed / verified contact option | Construct URL or promise immediate resend |
| Dispute or plan request | Pause ordinary nudges; billing owner review | Defend charge, threaten consequences, negotiate plan |
| Service occupant differs from authorized bill-to | Verify recipient authorization | Disclose balance based on address match |
| Final allowed touch exhausted | Stop and propose owner escalation | Continue indefinitely or reset touch count |
| Send accepted but delivery readback failed | Accepted/unknown delivery, reconcile | Claim delivered or blindly resend |
| Wrong-number plus hazardous work report | Suppress without account details and preserve internal hazard | Expose billing identity or drop risk |

## Source synthesis and timing decisions

The inventory contains one unique `rivetflo-csr-invoice-follow-up` main variant. Preserve its positive-balance entry gate, claimed-versus-verified payment distinction, trusted-link requirement, billing dispute escalation, negation handling and stop-before-happy-call rule.

The historical sequence was an initial due/overdue touch, then +3 / +7 / +14 days with final owner escalation. This package does not install that sequence or silently resolve whether those offsets mean anchor-relative days or delays since prior touch. Require explicit current tenant policy and cap; consent, human ownership, payment verification and source changes override any timer.

The latest default customer-service v1.1.0 policy supersedes “I'll get the link over shortly,” “someone will reach out shortly,” and other receipt-free promises. Record a payment claim without claiming a CRM note was saved; claim a billing handoff only after durable work-item readback. A trusted link must also belong to the correct tenant/invoice and authorized recipient. Zero balance is not always a payment, and satisfaction outreach remains a separate eligibility decision.

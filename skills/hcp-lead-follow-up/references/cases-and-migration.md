# Synthetic acceptance cases and migration decisions

All labels here are invented and are not valid provider identifiers. These are offline review fixtures, not evidence of runtime behavior or permission to create test customers.

## Worked draft

Input: tenant `example-service`, inquiry `synthetic-inquiry-A`, authorized service-area evidence, customer wants a repair and prefers `synthetic-window-A`; booking adapter is absent. Identity/consent may permit responding, but this run has no send approval.

Expected artifact excerpt:

```yaml
mode: draft
lead:
  intake_ref: synthetic-inquiry-A
  status: scheduling
  status_basis: proposed
  service_interest: repair
  urgency: unknown
  preferred_windows: [synthetic-window-A]
  booking_receipt: null
  booking_readback: null
outbound:
  reply_to_customer: "That is your preferred window; an appointment is not confirmed."
  state: not_sent
handoff:
  required: true
  receipt_ref: null
  readback_ref: null
decision: handoff_needed
next_step: Obtain an authorized scheduling or durable office-handoff capability.
```

The full artifact must also include scope, gate results, source references and unknowns from the evidence contract. This abbreviated example does not invent successful receipts.

## Acceptance matrix

| Synthetic input | Required result | Forbidden claim/effect |
|---|---|---|
| Selected window outside campaign recommendation but valid availability | Continue normal booking gate; recommendation alone is not rejection | Automatic out-of-window refusal |
| Selected slot now unavailable | Fresh verified alternatives or preferences/handoff | Silent substitute booking |
| Availability read succeeds; booking is disabled | Preference only; no hold receipt | “I've held/booked it” |
| Booking request times out | Lookup original action/receipt before retry | Duplicate appointment creation |
| New web submission duplicates a prior event with a different timestamp | Reconcile canonical inquiry and touches | Treat timestamp difference as new outreach permission |
| Existing-job callback under a lead-owned phone | Route authorized existing-job intent | Create a new sales journey by priority |
| “Wrong number” | Suppression required; neutral apology draft only if allowed | Customer name/address/service disclosure |
| “STOP, and there is smoke from the work” | No sales copy; suppression plus internal safety handoff, tracked separately | Dropping hazard because STOP won |
| Pricing absent in policy | Explain unverified price / office review | Invent fee, discount or financing |

## Source synthesis and meaningful variants

Reviewed both unique main variants of `rivetflo-csr-lead-handling`: the base family and the family adding campaign booking windows as recommendations. Both preserve minimal qualification, verified-slot selection and safe scheduling fallback; this package keeps the nonblocking campaign-window rule explicitly. It also retains the routing warning as a discovery requirement instead of claiming a particular legacy/unified service exists everywhere.

Both older variants suggested “check/hold times” or “office will confirm” when booking was disabled. Those implications are superseded by the newer default `rivetflo-csr-customer-service` v1.1.0 durable-receipt and consent policy: no hold, handoff, person assignment or timing promise without corresponding verified evidence. Cross-lane hazards, wrong-number handling, mixed STOP/hazard and explicit journey ownership apply even to an otherwise ordinary lead.

No universal lead cadence is inferred. Company, trade, service area, pricing, contact options and runtime bindings are deployment parameters. Source profile identities, private routing paths and real customer examples are intentionally excluded.

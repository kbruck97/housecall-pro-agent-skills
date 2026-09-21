---
name: hcp-lead-follow-up
description: "Use when qualifying HCP service leads or scheduling replies. Draft evidence-grounded follow-up with consent, ownership, and booking-receipt gates."
license: MIT
version: 1.0.0
---

# HCP lead follow-up

Turn a new-service inquiry into a qualified lead, verified booking, or truthful human handoff. Use for inbound service/sales calls, SMS, missed calls, web inquiries and replies to offered slots. This is a portable procedure, not an HCP integration or permission to contact customers.

**Default: read-only analysis and unsent drafts.** Discover actual adapters using [adapter and safety contract](references/adapter-and-safety-contract.md) before considering any effect. Read that reference in full for consent, cross-lane routing, durable receipts and failure handling. Record outcomes using [evidence contract](references/evidence-contract.md). Use [synthetic cases and migration decisions](references/cases-and-migration.md) for acceptance review.

## Inputs and entry gates

Require a tenant alias, approved company label, authorized inquiry/source reference, dated source/conversation evidence and the tenant's service area/intake policy. Outbound additionally needs a verified endpoint, channel/purpose permission, current owner and approved send policy. Do not invent a lead ID for an anonymous inquiry; retain its authorized intake reference and mark customer linkage unknown.

Supply tenant-specific timezone, quiet hours, trade/service boundaries, approved pricing/disclosures, escalation destination and contact option where available. A cold intake wrapper and an established-conversation agent may own different paths: discover actual routing, not an assumed unified runtime. Existing-job repairs, reschedules, billing and complaints are not automatically new leads.

## Procedure

1. **Resolve scope and ownership.** Match the inquiry to authorized tenant/customer/property candidates using actual adapter formats. Read previous messages and active journeys; distinguish a new submission from replay. Existing contact history is context, not permission to rearm a closed or suppressed campaign. If another agent/human owns the conversation, prepare a handoff instead of sending competing copy.
2. **Classify all intents before qualification.** Opt-out, wrong-number, safety and complaint gates override sales copy. Preserve an internal safety handoff even with STOP. Billing, estimate revisions, warranty claims, cancellations and return visits go to their proper service/billing owner, not a duplicate sales journey.
3. **Collect the minimum useful facts, naturally.** Ask one missing question at a time: need/project, relevant service location/area, urgency, preferred windows, then access or useful photos. Reuse verified name/contact details rather than requesting them again. Capture decision-maker, prior-customer or warranty context only if needed. Never diagnose from symptoms or solicit unnecessary private information.
4. **Qualify against evidence.** Check service area and supported work; if unknown, mark for review rather than reject or promise coverage. Quote exact pricing, fees, discounts, financing or warranty only from approved current policy/source evidence; otherwise prepare a human question. Angry replies, missed callbacks, unusual approval requests and safety concerns need escalation. A simple choice of another provider is a no-pressure decline/closure, not automatically a hard escalation; preserve any accompanying complaint or safety concern separately.
5. **Offer availability only when verified.** A tenant/property/service-appropriate availability read may support two or three concrete slots, with timezone and expiry/freshness. Otherwise collect preferences. Campaign booking windows are preferences, not hard service availability: do not reject an otherwise valid customer-selected slot solely because it falls outside a campaign window. Actual service hours, territory and capacity constraints still apply.
6. **Process slot selection honestly.** Refresh the selected slot. In draft/read-only mode, acknowledge preference without claiming a hold or booking. If authorized booking is supported, check for an existing appointment, use the documented idempotent booking operation and verify the exact appointment after writing. Only a matching receipt/readback permits `booked`. Stale slots require fresh options, not substitution without customer agreement.
7. **Handoff or continue.** Include issue, urgency, known facts, missing facts and preferred windows. Only a verified durable handoff permits “I've sent your preferred window to the office for review.” Do not say the office will confirm or call soon without a real commitment. Without a receipt, describe the request as unconfirmed and use only a verified tenant contact option.
8. **Emit evidence, then stop.** Store an unsent draft, proposed status, precise next action and failures. On authorized execution, read back each changed target and keep booking, handoff and message delivery as separate effects. Follow-up timers require approved configuration and must stop on suppression, human ownership, booking or closure.

## Journey-specific evidence

Add to the common artifact:

```yaml
lead:
  intake_ref: <authorized inquiry reference>
  source_channel: <call|sms|web|other>
  status: <new|qualifying|scheduling|booked|handoff|lost>
  status_basis: <proposed|verified>
  service_interest: null
  service_area_check: <pass|fail|unknown>
  urgency: <emergency|same_day|this_week|flexible|unknown>
  preferred_windows: []
  missing_facts: []
  availability_read_ref: null
  selected_slot_ref: null
  hold_receipt: null
  booking_receipt: null
  booking_readback: null
  linked_existing_job_ref: null
```

`lost` requires an actual decline or approved closeout policy; silence is not rejection. A draft-only status must not be mistaken for a saved CRM update. `booked` requires authoritative booking evidence, not a chosen slot or sent SMS.

## Safe draft patterns

- Unknown need: “Hi, this is {company_name}. What can we help with?”
- Need known, location missing: “What area is the service needed in?” Ask for the full service address only when necessary and authorized.
- Preference received, no booking: “That is your preferred window; an appointment is not confirmed.”
- Unknown pricing: “I don't have a verified price for that scope.” Add a verified contact option or receipt-backed handoff, never a fabricated quote.

These are drafts, not permission to send. Do not include customer facts before identity/consent gates pass.

Read [public data operations](references/public-data-operations.md) for documented endpoints and state boundaries.

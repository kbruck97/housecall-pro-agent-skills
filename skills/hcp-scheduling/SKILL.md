---
name: hcp-scheduling
description: Use when scheduling field-service visits. Verify property, pricing, availability and authoritative booking receipts.
license: MIT
version: 1.0.0
---

# HCP scheduling

Use for availability, appointment choice, maintenance/service-visit pricing and booking/change requests. This package provides a portable workflow, not a claim that HCP exposes these functions universally. Follow [adapter and receipt gates](references/adapter-contract.md) and [pricing and settlement](references/pricing-and-settlement.md).

## Ordered procedure

1. **Discover capability.** Confirm actual schemas for context, availability, quote, booking, current appointment readback and escalation. Bind tenant policy and calendar to the same authenticated tenant. No verified adapter means intake/draft only.
2. **Resolve context and property.** Read same-turn authorized customer context or retrieve it. Multiple/concatenated service addresses require explicit selection before quotes or slots. Billing address is not service property. Capture appointment type, service need, access constraints and urgency.
3. **Apply maintenance intake policy.** Equipment-priced visits need a current confirmed equipment list and quantity. Let the customer correct old records without arguing; mark corrections as reported rather than silently overwriting equipment. Onsite-assessment visit policies may require address only and deliberately skip equipment questions. Do not universalize one tenant's intake.
4. **Quote accurately.** If full price is requested before scheduling, obtain the full quote first. Otherwise obtain availability and its verified disclosure. In every case disclose applicable maintenance price/qualifications before booking. Partial/unit fees are not total prices; member terms require verified membership. Stop for unverified required price rather than claiming a final total.
5. **Get availability.** Use the customer's preferred window, confirmed scope and configured timezone. Offer a small choice of returned slots exactly, with unambiguous local day/time and duration/arrival-window distinction. A requested time is not availability. Do not derive openings from historical calendars or hardcoded weekday grids.
6. **Record acceptance.** Bind the customer's choice to the exact returned slot/capability and quote revision. Preserve opaque tokens exactly. If scope, equipment, address, price or slot freshness changes, recheck affected evidence and seek renewed acceptance.
7. **Book once when authorized.** Use transport-bound tenant/party/property, immutable attempt key and exact slot capability. Check prior attempt/receipt before submitting. Customer reconfirmation is not permission for a second booking. Prefer atomic reservation/idempotency supported by the adapter.
8. **Settle and read back.** Final booking needs a final authoritative status and provider appointment reference, then exact current-state readback. Pending, dry-run, refused, timed out or generic “ok” without a verified contract is not booked. Do not retry unchanged after errors or resend after ambiguous success.
9. **Render truthful confirmation.** Name only the verified day/time/window and known commitments. Reminders, technician assignment or callback timing need their own evidence. A pending durable request may be described as recorded but no promise the office will confirm “shortly.”

## Stop conditions

Concrete hazard, essential-service outage requiring urgent dispatch, price dispute, uncertain membership, unsupported multi-system scope, wrong tenant, missing calendar policy or uncertain booking state means routine scheduling pauses. Vague “emergency” alone calls for symptom/urgency clarification, not invented danger scenarios. Escalate through the authorized monitored channel with receipt truth; consent may suppress customer copy but not internal safety.

## Output

Return the common envelope plus property confirmation, service/equipment scope, quote status/disclosure reference, offered slot references, customer acceptance evidence, booking attempt status, provider readback, and exact draft customer copy. A scheduling request, held slot, final booking and delivered confirmation are separate outcomes.

Read [public data operations](references/public-data-operations.md) for documented endpoints and state boundaries.

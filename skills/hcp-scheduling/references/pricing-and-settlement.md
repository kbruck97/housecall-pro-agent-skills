# Quote semantics and booking settlement

## Pricing source contract

Discover actual field names rather than assuming these semantic labels are tools. For every quote retain authenticated tenant, service property, appointment type, equipment/quantity if relevant, membership status, quote revision, freshness, currency, fee composition, confidence/quotability, final/partial/refused state and exact approved disclosure.

- **Full equipment-plus-dispatch maintenance:** tenant policy may total equipment lines plus a maintenance dispatch tier based on verified travel inputs. Unit maintenance pricing excludes dispatch unless explicitly stated. Do not substitute a diagnostic fee table.
- **Drive-tier visit total:** tenant policy may include travel in the visit total while materials remain technician-assessed. Preserve that caveat; no extra dispatch charge and no invented all-inclusive materials promise.
- **Service diagnostic fee:** covers only its stated travel/diagnostic scope, not repair, parts, install or replacement cost.
- **One-time unit price:** require a current, quotable authoritative result; do not promote a unit price to a whole visit. A stale cache, inactive item, missing mapping, ambiguous taxonomy or unexplained zero requires review.
- **Membership:** do not infer plan status from relationship history. Verify current agreement, covered scope and disclosure. Never promise discounts from old memory.

Keep canonical equipment keys exact as discovered. Compound equipment names may match generic substrings incorrectly; a tankless unit must not be priced as a storage tank or an additional head as a complete system. Conflicting customer equipment statements require a scoped quote correction, not an unapproved equipment database write.

No arithmetic by the language model. Any authorized calculation must use deterministic tooling and source-backed inputs; this workflow normally relays the verified quote verbatim. Missing maps/address may yield starting guidance but not a final travel fee.

## Attempt and readback schema

```yaml
schema_version: 1
mode: draft_only
tenant_ref: tenant_example
party_ref: party_example
property_ref: property_example
service_type_ref: service_example
intake_policy: office_review
equipment_confirmation: null
quote:
  status: unavailable
  revision: null
  disclosure: null
  scope: null
availability:
  observed_at: null
  timezone: null
  slot_refs: []
  expires_at: null
acceptance: {inbound_ref: null, selected_slot_ref: null, quote_revision: null}
attempt: {key: null, state: not_attempted}
booking: {provider_ref: null, state: none}
readback: {source_ref: null, observed_at: null, matches: null}
followup_receipt: null
customer_copy: null
blockers: [adapter_not_discovered]
```

Opaque references above are synthetic documentation aliases. Runtime provider IDs stay literal and access-controlled. Do not “repair” malformed identifiers; fail format validation and resolve through authorized discovery.

## Settlement state machine

- `not_attempted` → verified scope/quote/slot and accepted choice → authorized `attempted`.
- `attempted` → provider final receipt → exact readback → `confirmed_current`.
- `attempted` → pending request with durable monitored follow-up → `pending`; no automatic rebooking.
- `attempted` → timeout/unknown → reconciliation using original attempt key. Late results must be owned by a durable reconciliation task; an immediate empty lookup does not prove failure.
- `attempted` → explicit refusal/window rejected → refresh current availability or hand off; do not repeat identical input.
- Duplicate replay returning existing booking → read that booking; never create another.

A creation receipt may later disagree with current reschedule/completion/cancellation. Current provider truth wins for present-tense statements; retain original receipt as historical evidence. Reschedule/cancel adapters need independently verified semantics; do not emulate a destructive cancel-and-create sequence without approval and failure planning.

## Synthetic acceptance matrix

| Fixture | Expected behavior |
|---|---|
| Two properties, customer requests any opening | Ask which property; no slots or total yet |
| Equipment-priced policy, customer corrects list | Use corrected reported list consistently; no silent equipment mutation |
| Onsite-assessment policy, annual maintenance | Address/quote/material caveat; no unnecessary equipment interrogation |
| Requested time absent from returned slots | Explain unavailable result and offer actual alternatives |
| Partial quote has numeric subtotal | Do not present it as final total |
| Member status unverified | No member discount or standard one-time price presented as plan terms |
| Pending/dry-run result with provisional time | Not booked; no “office will confirm shortly” |
| Final status without provider reference | Incomplete confirmation evidence |
| Timeout then late success | Reconcile original key; exactly one booking |
| Customer says yes twice | Reuse/read prior attempt; no duplicate |
| Provider readback slot differs from generated copy | Block/correct copy before send |
| Ambiguous daylight-saving local time | Explicit timezone/offset and authoritative slot; no mental conversion |
| Scheduling client tenant differs from policy tenant | Refuse cross-tenant execution |

## Migration decisions

Source scheduling coordinator has one main variant. Its context/property/availability/price/booking order and exact slot/idempotency lessons are retained. Newer HVAC pricing references strengthen full-total versus unit-fee distinctions; the water-treatment overlay contributes onsite-assessment and travel-included pricing. Removed universal named tools, fixed calendars, technician names, third-failure retry quotas, “every inbound gets a reply,” automatic reminder promises and pending “shortly” language. Unsupported tools mean blocked capability, not fictional endpoint support.

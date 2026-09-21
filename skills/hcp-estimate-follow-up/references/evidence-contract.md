# Decision evidence contract

This is a portable artifact schema, not a provider request payload. Map it explicitly to discovered adapters. Use null for unknown scalar facts and empty lists for no evidence; do not invent references. Enum values separated by `|` below are alternatives, not literal values. All timestamps in real artifacts must be offset-qualified; include the tenant timezone for scheduling.

```yaml
schema_version: 1
mode: draft # draft | approved_write
tenant_key: <authorized tenant alias>
policy:
  version: <approved version or null>
  timezone: <configured IANA timezone or null>
  cadence_ref: null
  approval_ref: null
scope:
  customer_ref: null
  property_ref: null
  source_kind: <lead|estimate|invoice>
  source_ref: null
  journey_ref: null
  owner_ref: null
  authorization_evidence: []
source_evidence:
  - ref: <snapshot or authoritative read receipt>
    provider: <actual adapter provider>
    observed_at: <offset-qualified timestamp>
    source_updated_at: null
    fields_used: []
    freshness: <current|stale|unverified>
intent:
  primary: <semantic intent>
  secondary: []
  customer_statement: null # minimum necessary paraphrase/quote
consent:
  state: <allowed|denied|unknown>
  channel: <configured channel>
  purpose: <approved purpose>
  evidence_ref: null
  suppression: <not_needed|required|pending|verified>
  suppression_receipt: null
  suppression_readback: null
gates:
  identity: <pass|fail|unknown>
  source_eligibility: <pass|fail|unknown>
  consent: <pass|fail|unknown>
  ownership: <pass|fail|unknown>
  quiet_hours: <pass|fail|unknown|not_applicable>
  cadence: <pass|fail|unknown|not_applicable>
  approval: <pass|fail|unknown>
actions:
  - kind: <draft_reply|handoff|suppress|send|update_journey|book>
    idempotency_key: null
    adapter_binding_ref: null
    state: <proposed|blocked|requested|accepted|persisted|verified|failed|unknown>
    receipt_ref: null
    exact_target_readback_ref: null
outbound:
  reply_to_customer: null # exact DRAFT copy or null
  state: not_sent # not_sent | accepted | delivered | failed | unknown
  provider_receipt: null
  delivery_readback: null
handoff:
  required: false
  reason: null
  destination_ref: null
  receipt_ref: null
  readback_ref: null
  timing_commitment_ref: null
cadence:
  observed_touch_count: null
  cap: null
  next_eligible_at: null
  paused: true
  pause_reason: draft_mode
decision: <draft|blocked|suppressed|waiting|handoff_needed|handoff_verified|closed>
next_step: <specific operator or adapter action>
unknowns: []
```

## Validation rules

- `mode: draft` requires every action to be proposed/blocked and outbound to remain `not_sent`; reading an existing receipt does not mean this run created it.
- A `verified` action must contain both an actual receipt and matching exact-target readback. Copy cannot claim an effect beyond that evidence.
- Denied or unknown consent forbids ordinary outbound dispatch regardless of eligibility. Mixed risk remains in `intent.secondary` and `handoff.reason` even when the reply is null.
- Closed journey is not necessarily a changed HCP record. Keep local proposed disposition, durable journey state, and authoritative business state separate.
- An approved send must pass identity, source eligibility, consent, ownership, timing/cadence where applicable and approval gates at send time.
- Record unknown or incomplete pagination; do not infer absence of another journey from a partial listing.
- Report adapter failures and unverified persistence honestly; never populate invented receipt identifiers to satisfy a validator.

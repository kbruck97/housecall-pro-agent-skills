# Adapter discovery, evidence and synthetic checks

## Capability worksheet

Before execution, record for each capability its actual installed binding, request/response schema version, tenant/account selector, permission, freshness policy, evidence location, side effects and unavailable behavior:

| Conceptual capability | Minimum contract | Default if unavailable |
|---|---|---|
| Job/payment read | Exact customer/property/job and invoice links, completion, settlement, balances, timestamps and pagination | Block qualification; draft with missing facts |
| Consent/ownership read | Channel and purpose scope, opt-out/wrong-number, active human owner, cross-lane suppression | Block outreach |
| Journey/receipt read | Item-scoped ordered history, operation/provider IDs, actual status | No new touch if duplicate/unknown outcome |
| Task/escalation write | Explicit approval, tenant-bound idempotency, urgency mapping, durable task ID and exact readback | Task draft only |
| Messaging | Exact approved body/recipient/channel, final gates, atomic idempotency, provider receipt/status readback | Draft only |
| CRM note/recognition write | Approved exact target and payload, receipt/readback | Note draft only |

Tool availability is not authority. No invented universal `send`, `escalate` or HCP endpoint is supplied. An offline export supports historical analysis, not a fresh send gate. Keep credential values outside artifacts.

## Minimum private evidence object

Schema notation below is descriptive, not a vendor request. All fixture values are synthetic tokens.

```yaml
schema_version: 1
tenant_ref: synthetic-tenant
journey_ref: synthetic-journey
job_ref: synthetic-job
customer_ref: synthetic-customer
property_ref: synthetic-property
mode: draft
sources:
  - evidence_ref: synthetic-job-snapshot
    adapter_kind: supplied_fixture
    observed_at: null # real operation requires timestamp + freshness judgment
qualification:
  completed: true
  final_invoice_settled: true
  job_balance_zero: true
  source_conflicts: []
consent:
  channel: sms
  purpose: satisfaction
  status: unknown
  evidence_ref: null
ownership: unknown
rating:
  instrument: satisfaction
  scale: [1, 10]
  score: null
  source_message_ref: null
branch: blocked
block_reasons: [consent_unknown, ownership_unknown]
actions:
  - kind: opening
    state: drafted
    operation_key: synthetic-opening-key
    approval_ref: null
    task_receipt_ref: null
    provider_receipt_ref: null
    readback_ref: null
next_safe_action: verify_consent_and_owner
```

Require source timestamps for operational evidence; use `unknown` rather than false for absent facts. Carry raw IDs only inside protected tenant evidence stores, using redacted references in reports. Every conclusion must cite a source ref. Every receipt must bind tenant, exact target, operation key, payload hash, status and timestamps; approval must bind scope and expire. Store readback status separately from provider acceptance.

Private outcome record additionally includes verbatim feedback ref, unresolved issues, actual owner, accepted commitment/window, resolution evidence, review state (`not_requested`, `drafted`, `sent`, `customer_reported`, `verified`), referral consent/context and internal recognition. A CRM note draft summarizes only supported facts in one or two sentences. Missing receipts remain missing, not synthesized.

## Implementation invariants retained from variants

- Append later touches to the existing job/item session; preserve original facts, opener and turn order.
- Derive scanner cap, runner intervals, close behavior and copy stages from one cadence definition. Test the whole scan→send-result→scan round trip offline, not independent tables that disagree. Scan and simulate the first attempt, assert its configured next due date, and feed the resulting persisted state back into the scanner for every later touch. Require each configured intended attempt to become eligible when due and all consent/ownership/send gates still pass. On the final touch, require a terminal status/outcome and a cleared or neutralized due date, then rescan to prove no further touch is eligible. A neutralized due date must be demonstrably non-actionable to the scanner, not merely hidden in the display. This no-response lifecycle assumes confirmed transport outcomes; ambiguous sends still require reconciliation, not inferred success or a retry. These are configuration-driven assertions, not default intervals or a fixed attempt count.
- Persist a provider-message→CRM-row mapping before relying on eventually consistent remote column searches. Early callbacks must update the same row, not create duplicates.
- Apply provider-specific monotonic status transitions: late `sent` cannot regress `delivered`. Conflicting terminal events require reconciliation, not arbitrary numeric ranking.
- Persist transport outcome independently of CRM sync. If send succeeded and CRM update failed, repair the log under separate authority, never resend.
- On timeout, use the same operation key and readback/find-existing contract before any retry. On receipt persistence failure, stop and reconcile; do not assume failure to send.
- Optional separately commissioned voice needs a distinct attempt ledger, no-answer/voicemail outcomes, transcript/structured-result correlation and complete runtime variables. Provider tool payload formats must be discovered, not copied from historical examples. Booking requires its own exact receipt even if a voice session ends before a summary call.

## Synthetic regression matrix

These are expected outcomes, not claims of executed runtime tests.

| Fixture | Required result |
|---|---|
| Completed job; deposit paid; final balance positive | No outreach; settlement blocker |
| Settled old job and future appointment share phone | Bind old job by ID; never describe future work as complete |
| Paid complete job; unknown consent | Draft allowed; send blocked |
| Positive warmup, no concern | Single rating question; no fabricated score |
| Warmup says “debris remains” | Recovery; score null; no survey/review/referral |
| High score then technical question | Capture/handoff; no survey restart |
| Task write times out | `handoff_unconfirmed`; no callback promise; reconcile |
| Task persisted, nobody accepted | May report task recorded; no date/dispatch promise |
| Wrong number arrives in another lane before bump | Suppress bump across lanes |
| First bump then first inbound reply | Same session, original facts intact |
| Configured no-response cadence; confirmed synthetic results; gates pass | Feed each resulting state back into scanner; every intended attempt becomes eligible at its configured due time; final touch settles terminal status/outcome and clears or neutralizes due date; later scans remain ineligible |
| Scanner cap blocks a configured later attempt | Regression fails even if separate scanner and runner unit tests pass |
| Final touch leaves an active status or live due date | Regression fails; require terminal status/outcome plus cleared or neutralized due date and no later eligibility |
| Final-touch transport timeout or receipt persistence failure | Reconcile same operation key; do not fabricate terminal success or resend |
| Delivered then late sent callback | One message/CRM row; stays delivered |
| Review sent but display says awaiting office | Audit receipts; never repeat link automatically |
| Customer praises a technician | Private recognition draft, not public testimonial |
| Referral names another person | No unsolicited contact to named person |
| Active danger during high-score conversation | Stop marketing; urgent safety/human route |

## Editorial reconciliation

Four main happy-call variants and both implementation-note variants contributed: newer standalone tenant identification, neutral complaint empathy, corrections/question precedence, configured incentives and append-only cadence lessons were retained. Conflicting timing, older AI-voice defaults, arbitrary pause acknowledgments, unsafe equipment-manipulation scripts and hardcoded identities/incentives were removed or made opt-in contracts. Front-office and scheduling references contributed lane separation, exact booking receipts and partial-success handling only; they do not broaden this package into inbound intake or scheduling authority.

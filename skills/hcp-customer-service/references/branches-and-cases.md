# Branch procedures, evidence and failures

## Branches

**General question:** cite approved policy/source context. If unavailable, admit it. A verified public office contact may be offered; never invent the number. Without a handoff receipt, say “I don't have a verified answer to that,” not “I've sent it over.”

**Reschedule/cancellation:** identify the exact current appointment/property; clarify requested change once. Do not cancel the old booking first and then hope a new slot works. Discover adapter atomicity, authorization and rollback limits. A submitted change request is not a changed calendar; read authoritative current state before confirmation.

**Arrival/status:** current dispatch/provider evidence owns ETA and assignee. Old completion notes, original creation receipts and customer-proposed times are not current state. An internal case requesting an update does not prove a technician has been contacted.

**Existing-job/warranty:** record symptom, relevant visit and customer account without diagnosing or guaranteeing free work. Useful photos are optional and must not ask the customer to approach a hazard. A return visit is not implied by warranty concern.

**Billing:** stop routine collection persuasion. Fetch authoritative invoice/balance only within scope; a paid claim, plan request, refund or dispute needs billing review. Do not defend or change charges or ask for card details in chat.

**Complaint/communication breakdown:** retain alleged event versus confirmed facts. “Nobody called back” triggers review of delivered ledger and case ownership, not another unsupported callback promise. Repeated messages should update the existing monitored case when identity/risk match; distinct hazards must not disappear under dedupe.

## Case evidence schema

```yaml
schema_version: 1
case_ref: case_example
status: proposed
category: existing_job_issue
party_ref: party_example
property_ref: property_example
journey_ref: journey_example
customer_words: "The problem came back after the visit."
verified_facts: []
disputed_facts: []
source_refs: []
risk: {level: needs_review, basis: customer_report}
requested_resolution: null
preferred_callback_window: null
primary_handoff: {receipt: null, monitored_queue: null}
secondary_sync: {state: not_attempted, receipt: null}
human_assignment: null
automation_holds: []
customer_copy: "I'm sorry this is still concerning. What is happening now?"
customer_copy_status: draft
next_operator_step: review source visit and current symptom
```

Public examples use synthetic aliases only. Runtime records may contain minimal necessary protected details under access control; summaries must redact them. Customer report is evidence of the report, not proof of technical causation.

## Synthetic cases

- Concern about an efficiency sticker: acknowledge uncertainty and route model-specific review; no admission of unsuitable equipment, no technical interpretation from memory.
- Wrong number attached to an unpaid invoice: at most “Sorry about that,” under acknowledgment policy; no intended name, balance or service address. Persist suppression and record any failure.
- STOP plus flooding: suppress all ordinary customer outbound and create the internal urgent case independently; no promotional acknowledgment.
- Pending appointment change: “Your change request has been recorded” only with that receipt; no “You're rescheduled.”
- Escalation adapter returns success but monitored queue readback is absent: hold completed-handoff copy, mark settlement unknown and reconcile the same attempt.
- Primary monitored case readback succeeds, task-board mirror fails: truthful primary receipt, explicit operator sync blocker, no duplicate case/send.
- Customer chooses another provider without complaint: estimate decline owner, not automatic hard escalation. If they allege damage too, preserve customer-service risk.

## Historical conflicts resolved

The newer default customer-service variant contributes durable receipts, semantic cross-lane selection, wrong-number suppression and STOP-plus-risk handling. The equipment-service variant contributes neutral empathy and non-admission of unverified allegations. Older water-treatment/general variants contribute concise intake but their “shortly” promises are removed. Historical freeform safety and categorical tenant prohibitions are not copied as repair scripts; no technical troubleshooting is authorized here.

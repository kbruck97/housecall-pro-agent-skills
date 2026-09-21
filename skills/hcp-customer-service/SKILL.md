---
name: hcp-customer-service
description: Use when handling existing-job support and complaints. Capture facts, route risk and verify human handoffs.
license: MIT
version: 1.0.0
---

# HCP customer service

Use for existing-job questions, arrival uncertainty, appointment changes, warranty concerns, complaints, billing confusion and human assistance. Default to read-only evidence review and drafting; follow [adapter/consent contract](references/adapter-contract.md) and [branches and cases](references/branches-and-cases.md).

## Procedure

1. Bind authorized tenant, party and journey using current context. Read the latest delivered thread, active owner, consent and source job/appointment/invoice if needed. Do not ask for already-known details or reveal records before identity is sufficient.
2. Detect cross-lane wrong number, opt-out and concrete risk before ordinary support. Vague “emergency” warrants urgency/symptom clarification, not invented gas/fire scenarios. Concrete danger must not wait for routine intake.
3. Record only necessary details: issue in customer's words, relevant service property/source reference, urgency, preferred contact window and useful photos/access instructions. Keep allegation, verified observation and inference separate.
4. Answer supported general questions briefly. For absent/conflicting facts, state uncertainty; do not diagnose, interpret labels/contracts beyond evidence, promise warranty coverage or invent technician ETA.
5. Use a verified domain adapter only for explicitly authorized support actions. Appointment cancel/reschedule, invoice changes, employee assignment and record correction are separate writes—not consequences of conversational acknowledgment.
6. If unresolved/risky, prepare a concise case with the customer words, verified facts, open question, risk, current owner, exact copy already delivered and requested next step. With authorized escalation capability, create/update the monitored primary case idempotently and read it back.
7. Pause ordinary follow-up through an authorized workflow control; log its receipt separately. Without the capability, hold outbound locally and flag unverified upstream pause. Do not tell the operator “all automation stopped” when only one lane is held.
8. Gate customer acknowledgment on consent and receipt truth. One factual holding response may be appropriate; do not continue autonomously while a human owns the case. Forward new urgent details internally.

## Escalation boundary

Safety concerns, active leaks/flooding, smoke/sparks/shock, gas/CO concerns, structural risk, loss of essential service, unsafe-water/illness concerns, property damage, billing/legal disputes, repeated complaints and communication breakdown need human review at tenant-approved urgency. Public-review threats are reputation/support escalation, not permission to pressure the customer. Do not troubleshoot dangerous systems or substitute the office for emergency assistance. Context-appropriate immediate protective guidance should stay brief, avoid technical repair steps and not delay professional/emergency help.

## Truthful empathy

Acknowledge the person's frustration or need for clarity without asserting unverified fault, causation or diagnosis. Equally, do not deny documented harm or hide verified mistakes. Avoid defensive brand speeches. State only a verified next step; “I have sent this for review” needs a monitored case receipt and “someone will call today” needs a separately supported commitment.

## Return artifact

Use the common evidence envelope plus `category`, `customer_words`, `verified_facts`, `disputed_facts`, `urgency`, `handoff_owner`, `automation_hold_receipts`, `authoritative_mutation`, `next_operator_step`, and exact `customer_copy` or null. Preserve request, attempt, primary case creation, human assignment and resolution as distinct states.

For adjacent integration work, read [disputed-review investigations](references/review-dispute-evidence.md); its separate authority gates remain mandatory.

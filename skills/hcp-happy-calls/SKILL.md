---
name: hcp-happy-calls
description: "Use when drafting post-payment satisfaction follow-ups. Qualify completed paid jobs, route recovery, and require consent and durable receipts."
license: MIT
version: 1.0.0
---

# Post-payment satisfaction journeys

Produce a grounded check-in draft, response playbook, and private outcome record for a Housecall Pro (HCP) job. Default to **local draft/read-only**. A request to draft, scan, simulate, or “run a happy call” does not itself authorize messaging, ticket creation, CRM writes, booking, or automated voice provisioning. This package supplies procedures, not an HCP or messaging client.

## Inputs and adapters

Resolve tenant, exact job/customer/property relationship, completion evidence, final-invoice settlement and job balance, message history, contact consent/suppression, active conversation owner, brand voice, timezone, and approved cadence. Missing facts may remain placeholders in an explicitly labeled draft; they block customer-ready execution. Do not require a technician name if unknown; omit it rather than invent one.

Read [adapter and evidence contract](references/adapter-and-evidence-contract.md) before binding tools. Discover actual available methods, schemas, permissions, tenant isolation, freshness limits, task receipts, and readback behavior. A conceptual capability in this package is not a callable tool name. If no authorized adapter exists, use supplied exports and report their age; do not improvise endpoints or write probes.

## Procedure

1. **Set mode and scope.** Choose SMS draft by default, human voice script if requested, or synthetic roleplay. Identify the exact tenant and job; never use a shared phone thread alone as job identity. Automated voice remains off unless separately commissioned and expressly permitted.
2. **Qualify the event.** Require completed work AND settled final invoice AND no positive job balance. A deposit, payment claim, zero draft invoice, or future appointment is insufficient. Unknown or conflicting payment/completion facts block outreach. Keep payment time, completion time, and observation time distinct.
3. **Apply higher-priority gates.** Current opt-out, wrong number, consent unknown, active human ownership, unresolved complaint, duplicate touch, owner-disabled workflow, or quiet hours override eligibility and old timing rules. Check all lanes, not only this journey. A service-message permission does not automatically authorize review/referral marketing.
4. **Read durable history.** Resolve existing item-scoped session, send receipts, inbound replies, escalation/task receipts and unresolved questions. Do not reseed a session for an unanswered bump. Do not infer delivery from a draft, queued row, or `review_asked` flag.
5. **Draft one standalone opening.** Name the verified business and recent work, then one question. No score in the first outreach. Synthetic template: “Hi [first name] — this is [business] checking in after your [verified work]. How is everything working?” Never deliver unresolved placeholders.
6. **Route the reply.** Follow [conversation and recovery](references/conversation-and-recovery.md). Safety/escalation and consent outrank questions; questions outrank a survey; complaints do not need a forced score. A positive or neutral response may lead to the configured rating question. Do not label a 1–10 satisfaction score as standard NPS; standard recommendation NPS uses 0–10 and a recommendation question. Preserve instrument and scale.
7. **Handle next actions truthfully.** Draft a recovery or question handoff. In an independently approved execution workflow, obtain a durable task receipt and exact readback before saying it was passed to the office. Task creation is not human acceptance, scheduled work, dispatch, or a promised response time. Never promise any of those without evidence for that exact claim.
8. **Separate public-review policy.** A score can inform service recovery, never select only happy customers for public reviews. Default review/referral automation off. Any optional review invitation must use a verified tenant URL, current platform-compliant non-selective policy and separate outreach authority; no incentives for reviews. Do not automate a post-recovery ask or re-score. See the reference for the legacy-policy conflict.
9. **Close with evidence.** Record score or `not_collected` (never infer a number), feedback attribution, open issues, current owner, actual versus proposed actions, and receipts. Leave the last word to a resolved pleasantry. Mark no-response closure only under the configured policy and verified attempt history.

## Cadence and modes

There is no universal send day. Historical variants used a next-day opener plus either a later day-four bump or a roughly 48-hour bump/five-day closure. Preserve them only as migration inputs, not active defaults. Require tenant-approved anchor, gap, maximum attempts, close rule, timezone and quiet hours in one contract. No cadence configured means draft only. Consent, receipts and ownership always override timing; no automatic pause acknowledgment after a fixed number of minutes.

Human scripts use the same branches with listening cues. Roleplay uses invented customers and ends with a debrief on factual claims, classification, consent and receipt-gated promises. Historical automated-voice integration ideas survive as optional adapter tests, not permission to attach this skill to a live agent.

## Deliverables and failure behavior

Return only requested artifacts, plus material blockers: opening/next-message draft; branch decision and evidence; private concise CRM-note draft; recovery/escalation/question task draft; optional referral-context and technician-recognition drafts. Distinguish **drafted**, **submitted**, **persisted**, **accepted by human**, **sent**, **delivered**, and **resolved**.

On uncertain send outcome, reconcile the existing operation before retrying. On task failure, state internally `handoff_unconfirmed`; do not claim the office will respond. On stale consent or source facts, stop. On active danger, stop the survey and seek urgent human help; do not wait for a score or receipt to give appropriate immediate safety guidance.

Use the synthetic regression cases in [adapter and evidence contract](references/adapter-and-evidence-contract.md) before approving any implementation. No network capability or production integration is verified by this package.

# Lifecycle reconciliation and journey-state audit

## Invoice truth

Join within a verified tenant using an exact invoice identifier and its job relationship. Invoice number is a fallback only when independently unique and corroborated; never match across tenants. Preserve source identifier strings.

Evaluate final settlement with explicit semantic mappings:
- invoice paid/settled status or payment evidence;
- nonpositive authoritative invoice due balance;
- nonpositive authoritative linked job balance;
- complete final-invoice scope, not a deposit or partial installment.

A local active invoice follow-up is a settled-mismatch candidate only when the necessary source evidence supports settlement. A paid invoice and positive job balance is a conflict/remaining-balance bucket, not a reason to send a happy call. Null balance is unknown, not zero. If job linkage or source data is unavailable, mark insufficient evidence rather than asserting the item is stale. Preserve currency and amount units in private evidence.

## Estimate truth

Read the exact parent estimate, relevant options and conversion relations from the verified adapter. Map customer approval/acceptance/won states explicitly; an internal/professional approval does not imply customer acceptance. Inspect conversion links on jobs to both parent and option identities if the adapter exposes them. A converted job can prove conversion even if an older parent label lags.

Report separate buckets: customer accepted; converted; professional approval only; open/declined; missing; ambiguous option relation. A customer SMS “yes” is not itself a source-system conversion. An accepted estimate can still require scheduling work, and must not continue nurture while that handoff is unresolved.

## Queue and read-model parity

Trace the read-only causal chain:

`source event -> authenticated ingress receipt -> dedup/processing result -> normalized lifecycle values -> source/mirror write receipt -> derived stage -> scanner eligibility`

For customer replies, trace:

`provider inbound -> conversation/item identity -> classification -> deterministic action -> task/state receipt -> read-model stage -> cadence suppression`

Inspect each actual runtime binding and gate separately. A dashboard may only reflect/proxy state; do not call it the realtime resolver without evidence. A handler in source code does not prove the active caller imports it or supplies the required client. Separate implemented, tested offline, deployed and observed-live findings. This audit never replays a production webhook to fill a gap.

Record event creation, ingress receipt, processing, source update and provider-send timestamps, including timezone and clock uncertainty. Absence of a local event is not proof HCP sent it. An unavailable ledger is an evidence gap, not proof of zero activity. Duplicate/event-order issues are proposed investigations, not permission to edit ledgers.

## Happy-call apparent “awaiting office”

A legacy outcome such as `Happy / review requested` plus `Customer replied` may derive an awaiting-office stage even when a conversational path already sent the link. Inspect:

1. Raw group/status/outcome/next-step and mapping version.
2. Exact related follow-up item, customer and job identities.
3. Ordered inbound/outbound messages, provider IDs and actual delivery states.
4. Item-scoped session branch, score facts, review flags and history.
5. Durable office task/escalation receipts and unresolved customer questions.

A session flag alone is not delivery. If verified delivery exists, report a display/next-step mismatch rather than proposing another link. If the customer then asked a question, name that as remaining office work. An approved later repair should use the normal task/state adapter with receipt/readback, not direct database edits; this scan only drafts it.

## Prior work versus upcoming work

Build an event table for each exact job: creation, schedule, completion, settlement, outbound request, provider delivery and inbound response. A future appointment beside a happy-call message in a customer-level timeline does not establish a routing error. Compare the message's job key and wording with the earlier paid completed job. Conversely, a valid old job key does not eliminate confusing wording: report factual eligibility and customer-facing ambiguity separately.

Do not swap a customer's identity because a partial-name search returned someone else. Resolve missing names through authorized stable IDs or ask the operator. Reports should use redacted references, not customer phone numbers or exported private conversations.

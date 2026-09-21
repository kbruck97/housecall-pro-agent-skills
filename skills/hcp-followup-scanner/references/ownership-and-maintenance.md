# Reminder ownership and optional equipment-maintenance scans

## Appointment surfaces

Create a matrix per tenant for these independent surfaces:

| Surface | Audit questions |
|---|---|
| Day-before reminder | Which system owns it? Is local generation disabled and final transport rejecting stale items? |
| Same-day reminder | Same questions; do not infer from the day-before setting |
| On-the-way event notification | Separate sender/gate, event identity, replay suppression and final source-truth check? |
| Customer-initiated appointment reply | Remains available unless separately suppressed for consent/safety? |

If HCP owns proactive reminders, report local reminders `disabled_by_owner_policy`, not “no appointments.” A producer returning zero does not protect against precomputed or manually supplied reminders reaching a generic runner. The accepted implementation pattern is producer exclusion plus final transport rejection, while preserving unrelated lead/reply/invoice/estimate/happy-call lanes. The scanner audits this pattern; it never changes the settings.

For stale sends, compare actual provider body/status/time with source job schedule/status, local cached slot, source update time and webhook receipt/processing times. Determine whether the move preceded the send and whether an event actually arrived. Verify the final live caller performs fresh source reads; a truth helper elsewhere proves nothing. Detect ghost items caused by global-board rather than tenant-board mapping.

An on-the-way sender independently needs authenticated ingress, stable event/transition identity, atomic replay suppression, exact conversation/item identity, final DNC and a fresh authoritative job/status/schedule read. External job key lookup alone is insufficient. Synthetic adapter tests should prove two identical events yield one fake provider call and a canceled/rescheduled event yields zero obsolete notices. These tests are requirements, not authorization for a live notification.

## Equipment/lifecycle-backed maintenance

A maintenance audience may live in an optional equipment/lifecycle data store rather than the follow-up queue. Discover its read-only adapter/schema and tenant taxonomy; do not assume a particular SQL table or HCP endpoint exists. Keep it a separate source in the report.

For a request such as “dormant or due customers with heating and cooling,” parameterize:
- tenant and as-of timezone/date;
- definition of dormant and engagement source;
- eligible active unit statuses and whether components count;
- required distinct physical-unit count and heating/cooling capabilities;
- approved lifecycle triggers, excluded triggers and maintenance-plan policy;
- removal, opted-out, do-not-contact and human-ownership exclusions.

A dual-purpose heat pump may satisfy both capability categories but is still one physical unit. Two equipment rows do not prove two units if one is a component or duplicate. Prefer canonical taxonomy; use natural-language heuristics only as labeled review candidates. Ambiguous categories remain unknown rather than broad substring matches. Do not turn equipment age alone into proven service need.

Historical policies used specific dormancy windows and omitted certain filter reminders. These are tenant choices, not universal defaults. Define them before evaluating due state. Compare due dates with a grounded database/application clock and record differences. Aggregate joined schedules by distinct schedule/unit/customer keys to prevent join multiplication.

## Minimal maintenance output

Private row: tenant/customer/property reference, classification source/confidence, distinct active units, heating/cooling capability counts, eligible due schedule count, earliest due date, dormancy reason, last engagement timestamp/source, plan state, suppression reasons and evidence refs. Omit names, full addresses, phones and email unless an explicitly authorized operational export needs them. Never place contacts in public drafts.

Report source coverage and unknown classifications. A maintenance candidate is not send permission or a clinical/technical diagnosis. No outbound lane is commissioned by an audience scan.

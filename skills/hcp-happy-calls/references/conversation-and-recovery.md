# Conversation and recovery rules

## Priority and state

Evaluate every new message, including messages after closure, in this order:

1. Consent withdrawal/wrong-number and immediate safety constraints. Suppress ordinary outbound activity across workflows; retain a new safety signal for authorized human handling without resuming a marketing journey.
2. Hard escalation or active human ownership.
3. Complaint/low rating requiring recovery.
4. Customer question requiring capture and handoff.
5. Survey continuation, optional policy-reviewed review/referral handling, or closure.

Suggested internal states are `draft`, `blocked`, `warmup`, `rating_pending`, `question_capture`, `handoff_pending`, `human_owned`, `recovery_pending`, `resolved`, `no_response`, and `suppressed`. These are package vocabulary, not promises about a vendor schema. Map them explicitly. No failed side effect advances the journey to a receipt-dependent state.

## Positive, neutral, and ambiguous replies

After a positive/neutral warmup, ask one configured question. For a legacy satisfaction instrument: “On a scale of 1–10, how would you rate your experience?” For recommendation NPS: use the approved 0–10 recommendation wording. Record which was asked. A 9 or 10 supports positive sentiment; a score of 8 or below can trigger a recovery check, but never invent dissatisfaction details. An ambiguous answer remains ambiguous; do not convert “great” into 10. A volunteered score need not be requested again.

A factual correction is not automatically a complaint. Acknowledge lightly, remove unsupported detail, and return to the customer's actual concern. Do not turn an ordinary correction into a formal apology or blame the office. “All good” after a correction can close the exchange without a recovery task. A final emoji/pleasantry needs no automated response.

## Questions outrank surveys

When the customer says they have questions but does not state one, draft “What questions do you have?” Once provided, preserve their words in a private task draft. Do not diagnose, interpret a nameplate, or answer operational/technical questions from sparse happy-call context. Do not resume rating/review/referral automation after handoff.

Receipt-gated wording:
- No task submitted: internal draft only; never “the office has it.”
- Durable task persisted and read back: “Your question has been recorded for the office.” This does not promise a response time or claim a person accepted it.
- Named owner accepted and committed a window: only then use that exact owner/window, subject to send approval.

The same distinction applies to a customer who first gives a high score and then asks a technical question. A high score does not cancel the question.

## Recovery

A complaint at warmup skips the numerical survey. Store `score: null`, `reason: concern_before_rating`, not an inferred low NPS. If no issue detail is given, ask one neutral clarifying question. If already stated, do not make them repeat it.

Empathy acknowledges concern without admitting unverified negligence, equipment error, damage causation, breach, or refund liability. Prefer “I understand why you'd want that checked.” Do not write “you're right, we installed the wrong unit” based solely on an allegation. Keep their claim and independently verified facts separate.

Classify proposed resolution by customer presence:
- `schedule_required`: indoor diagnosis/inspection or another visit needing access; availability and booking are a separate approved workflow.
- `execute_without_presence`: a verified exterior cleanup or similar task that requires no customer attendance. This classification alone does not authorize dispatch or a promised date.

A recovery task carries exact tenant/job/item scope, verbatim issue, proposed action, proposed owner, requested urgency, evidence and operation key. A receipt proves persistence only. Set a follow-up due time from a human-accepted commitment, not from an invented “end of today” rule. If no commitment exists, put it in the operator's unaccepted-work queue.

After verified technician completion, a separately authorized customer check can ask whether the issue is resolved. Technician confirmation and customer confirmation remain separate facts. Do not re-ask a score after recovery. If unresolved, keep the same recovery identity and route back to the owner rather than duplicate the ticket.

## Escalation and pause

Escalate safety risk, active water intrusion, significant property damage/compensation, billing disputes, legal/reputation threats, repeated complaints, communication breakdown and lost-confidence/competitor-switching concerns. Distinguish an identity question (“who is this?”) from a billing dispute; verify identity without revealing job details. Minor cleanup without risk, damage or repetition can remain recovery.

Urgency depends on harm, not mere vocabulary or the tenant's trade. Possible gas leak, carbon-monoxide alarm, fire/electrical danger, unstable structures or active destructive flooding need urgent human handling. Do not down-rank an actual emergency because the business services that equipment. Conversely, a routine service symptom is not automatically a life-safety event.

Give concise situation-appropriate safety guidance; avoid hazardous repair, valve, breaker or meter manipulation instructions. For immediate danger, direct the person to emergency services or the relevant utility from a safe place. A verified office number is not a substitute for emergency response. Do not claim a technician is coming without accepted dispatch evidence.

Draft an escalation with verbatim signal and explicit urgency mapped to the discovered adapter enumeration. A word such as “emergency” in free text may not set actual routing priority. Verify both persisted task and routing fields. Silence the survey during human ownership; forward new safety-relevant information as a distinct authorized alert, not buried in a summary. No elapsed-time rule independently authorizes another customer text.

## Reviews, referrals, and recognition

Legacy happy-call variants asked for public reviews only after 9/10 scores and described an operator-approved positive-resolution exception. This package deliberately does **not** preserve that as automated review selection: it creates review-gating risk. Survey scoring is for service improvement. Any review program must be non-selective by sentiment, verified against current destination rules, optional and separately authorized. Pause marketing during active support without permanently excluding unhappy customers from an otherwise uniform review program. No reward for a review or for revising/removing criticism.

Referrals are a separate message only under an approved tenant program and channel consent; never combine a review ask with a referral pitch. No default gift-card amount. A customer naming a relative does not give that relative permission to be contacted. Capture minimal referral context, prefer the customer sharing the business contact, and require fresh approval/consent for any later nudge. An old “two weeks” example is not a scheduler instruction.

Technician praise can produce a private recognition draft with source attribution. Public testimonial use needs separate rights/consent. “Customer says they posted a review” is `customer_reported`, not platform-verified publication.

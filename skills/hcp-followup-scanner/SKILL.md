---
name: hcp-followup-scanner
description: "Use when auditing due or blocked HCP follow-ups. Reconcile source truth, consent, receipts and derived stages without sending or mutating records."
license: MIT
version: 1.0.0
---

# Read-only follow-up scanner

Answer what is due, eligible, blocked, stale, awaiting humans or already resolved across leads, estimates, invoices, happy calls, appointments and optional maintenance. This is a **read-only audit**, not a sender, synchronizer, repair job or scheduler. Do not mutate CRM/HCP/store records, flip gates, replay production events, install cron, restart services, or send test messages.

## Discover before scanning

There is no universal follow-up database, stage formula, endpoint, CLI or environment flag. Identify the tenant's actual adapter contracts from operator-supplied configuration and available read-only capabilities. Record:

- tenant/account identity and exact source/store selector;
- source class (authoritative HCP read, local snapshot, control read model, CRM mirror, optional equipment/lifecycle store);
- schema version, semantic field mappings and stage derivation;
- authorization and proven read-only behavior, including whether a “dry run” logs or syncs anything;
- pagination, limits, timestamp semantics, timezone, freshness and rate/error handling;
- consent/ownership sources and message/task/provider receipt sources;
- workflow policy, reminder owner, cadence definitions and transport gates.

Prefer an established tenant-scoped read-only control reader if it resolves the current store accurately; otherwise use the verified active store, a proven no-write scanner, or an authorized source export. Do not prefer a stale control mirror over fresh authoritative lifecycle truth. If safe adapter discovery fails, analyze supplied fixtures or return the missing contract; do not guess private paths or endpoints.

## Workflow

1. **Freeze scope.** Name tenant, workflows, due cutoff, local timezone, as-of clock, freshness window and read-only authorization. Resolve identifiers exactly; do not silently substitute a similar name or repair malformed IDs.
2. **Resolve the active source.** Confirm tenant registry/config mapping and board semantics, not an old clone/store location or global default board. A valid path may still be the wrong tenant or a stale deployment.
3. **Collect comprehensively.** Exhaust pagination within scope; record cursors/pages, returned counts, truncation and missing-source errors. A limit of 25 is a sample, not a total. Preserve SQL nulls and distinguish unknown facts from false values.
4. **Derive queue state.** Use the same verified stage rules as the authoritative reader. Keep raw labels and derived stage together. A derived stage is not necessarily a persisted column. Positive conversation outcome does not always mean resolved: claimed payment or accepted estimate may still require office verification/action.
5. **Evaluate policy and safety.** Separate due-date eligibility from actual permission. Cross-lane opt-out/wrong-number, human ownership, replies, disputes, owner disablement, duplicate receipts and quiet hours block proactive work. `eligible_dry_run` never means sent. Consent unknown is blocked, not an empty flag to ignore.
6. **Reconcile HCP lifecycle and evidence.** Apply [reconciliation and state audits](references/reconciliation-and-state-audits.md). Authoritative payment/conversion/completion facts supersede stale queue labels; a mismatch produces a repair proposal only. Missing/partial data produces `unknown`, not “reconciled.”
7. **Audit ownership and maintenance separately.** Use [ownership and maintenance](references/ownership-and-maintenance.md). Proactive reminders, on-the-way notifications, inbound appointment replies and equipment-derived maintenance are distinct surfaces with different owners and gates.
8. **Explain actual remaining work.** Check delivered message receipts and item-scoped journey history before repeating a review-link task. Separate completed happy-call outreach from an unresolved technical question. Keep prior paid jobs separate from future appointments in a shared thread.
9. **Report counts and exceptions.** Use [evidence and synthetic checks](references/evidence-and-synthetic-checks.md). Reconcile denominators programmatically; show completeness, freshness, disabled workflows, unknowns and minimal redacted evidence references. Recommend the next safe operator action, never execute repairs as part of the scan.

## Storage safety

For approved SQLite inspection, open an existing file with URI `mode=ro`; plain `connect(path)` can create a missing file. Use a bounded read transaction, not direct updates. Do not delete/recreate databases, send ledgers or WAL/SHM sidecars. WAL-backed forensic snapshots require a consistent supported backup/snapshot including committed WAL state; copying only the main database or copying live sidecars at unrelated times is not a trustworthy snapshot. Any local snapshot output requires an approved protected report location.

For optional relational stores, use a genuinely read-only transaction/role and explicit tenant predicates on every join. Do not print environment or credential dumps. A scanner import or `--dry-run` label is not proof of zero side effects; inspect its contract first, or use exported fixtures instead.

## Stop conditions

Wrong/ambiguous tenant; unsupported identifier shape; unavailable consent/ownership truth; missing field mapping; stale or incomplete source; unknown stage rules; unsafe scanner effects; authorization failure; rate limit; or inconsistent counts must be visible in the report. Return a scoped partial audit if useful, with `completeness: partial`; never claim a zero backlog or universal reconciliation from a failed query.

All fixes require a separate approved workflow, exact targets, idempotency and readback. This package makes no current API-support claim.

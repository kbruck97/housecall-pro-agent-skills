---
name: hcp-alpha-data-collection
description: Use when HCP evidence collection needs scope-safe public or opt-in private alpha reads, pagination, and coverage receipts.
license: MIT
version: 1.1.0
---

# HCP evidence collection

## API-first execution preference

Use the supported public API when sufficient. For UI-backed tasks otherwise, prefer a verified authorized Alpha/internal-session API over UI clicking. Use the browser for secure login/MFA/session bootstrap, visual verification and unavailable routes, not as the default data transport. Follow the [authorized internal-session workflow](references/internal-session-workflow.md) before using a protected session; it covers tool capability gaps, isolated session jars, identity readback, current CSRF/header/schema checks, exact-operation approval and ambiguity recovery. Access denial is never permission to switch surfaces. No live auth adapter is supplied.

Collect evidence, not equipment decisions. Default to authorized read-only public capabilities; add private alpha/React reads only through an explicitly opted-in adapter. Neither surface is assumed complete. This package supplies procedures and data contracts, not an executable HCP client, authentication helper, or universal tool catalog.

## Preflight

1. Establish the exact tenant, requested job/customer/property, read purpose, coverage requirement, output audience, and allowed storage/retention. A customer-wide request is not authorization for a tenant-wide dump.
2. Select a configured adapter from [Adapter contract](references/adapter-contract.md). Require its declared read capabilities, authentication ownership, expected response shapes, pagination contract, and exact tenant guard. If no suitable adapter exists, report `blocked_adapter`; do not invent tool names or commands.
3. Validate source identifiers against that adapter's declared formats before lookup. Do not repair malformed tokens, use a display number as a canonical identifier, or mine unrelated nested IDs. Resolve ambiguous display numbers through an authorized exact lookup or request a canonical identifier.
4. Keep credentials in the host's secure authentication facility. Verify the active tenant and exact requested object before collecting children. A successful taxonomy read proves access, not tenant identity. Do not try arbitrary accounts to locate a customer.
5. Declare which evidence surfaces are required versus optional. Read-only mode prohibits create, attach, patch, delete, replay, and test-write operations. Evidence adjudication belongs to hcp-trade-equipment-job-review; optional downstream reconciliation is a separate authorization boundary.

## Procedure

1. **Capture a coverage plan.** Create an evidence bundle using [Schemas](references/evidence-schema.md). Every required surface begins `not_requested` or `pending`, never empty by default. Record a snapshot boundary and endpoint capability observations without bodies or credentials in logs.
2. **Read the root object and addresses.** Parse documented envelopes with type checks. Verify customer and property relationships. Resolve a service property from explicit job linkage, never a billing address or a recursive search through dispatch metadata. A null link may be resolved from a unique verified customer address with corroborating job location evidence; conflicting, ambiguous, or placeholder links remain unresolved.
3. **Enumerate exact jobs.** For full history, exhaust authorized customer-scoped public lists and, when opted in, private lists; preserve each source's set separately and union by canonical ID. Verify each row's customer before collecting children. Re-fetch union members individually; list membership alone is not proof of scope. Inspect discrepancies, including canceled, deleted, or stale-owner rows, without converting them into installation evidence.
4. **Prove pagination.** Keep request cursor/page, returned row count, unique IDs, duplicates, totals, terminal condition, and scope rejects. Parse top-level public `jobs` independently from private `data` envelopes. Nonzero advertised totals with no parsed rows are a parser failure. Repeated cursors, unknown envelopes, or changing totals block completeness. See the bounded recovery rules in the adapter reference.
5. **Gather per-job detail.** Collect status and actual finish timestamps, direct line items, notes, attachment inventory, and any required estimate or sibling-segment context. React line items may be a mapping of labor/material lists, not a list. Resolve estimate option and parent identities using declared adapter relationships, never guessed prefixes. Keep proposals and completion evidence separate.
6. **Gather existing equipment.** Enumerate every verified requested service property; normalize all page wrappers and verify each equipment row's property. Read relevant detail and job links where supported. An unavailable equipment surface stays unavailable even if public job reads work. A stale empty prompt or local cache is not an empty live inventory.
7. **Inventory and inspect media.** Reconcile job attachment metadata, explicit expansions, optional private attachment metadata, and customer-level attachments when in scope. Deduplicate attachment IDs and content hashes while retaining all source relationships. Classify each file as inspected evidence, UI artifact, context document, unreadable, expired, or skipped. A self-link is not an attachment. Avatars, logos, map pins, and brochures are not nameplates or installation photos.
8. **Minimize before persisting.** Use an allowlisted projection, not a raw JSON dump. Keep exact IDs and private object relationships in an access-controlled runtime index; export synthetic/local aliases and evidence summaries. Drop free-text identity/contact/payment/access details, arbitrary URLs, signed queries, filenames, and embedded map/avatar fields recursively. Preserve safe technical assertions only after review. Media derivatives require visual privacy review and metadata stripping before distribution.
9. **Close with a receipt.** Reconcile all required requests, exact-job detail reads, property gates, pagination, and attachment inspection states. Distinguish `complete`, `partial`, and `blocked`. Validate [Failure cases](references/failure-cases.md) and publish only the sanitized receipt and requested summary. A complete receipt is complete only within its declared surface/time scope, not proof of all data that could exist elsewhere.

## Stop conditions

Stop collection or the affected branch on tenant mismatch, unresolved source ID, denied private opt-in, credential leakage, unsupported envelope, repeated pagination, unbounded/global discovery, missing required data, or exhausted recovery budget. Report the exact failed capability and what remains unknown. On a private-session 401, refresh through the authorized adapter once and retry once; failure blocks private equipment conclusions. Public reads may continue for public evidence but never stand in for missing equipment reads.

Never turn a failed lookup into “no jobs,” an uninspected attachment into “no photos,” or a missing equipment adapter into “no existing equipment.” Do not broaden to tenant-wide reads without explicit authority. An exhaustive request with required unavailable surfaces cannot be marked complete.

## Verification and handoff

The receipt must show successful root scope proof; each required surface's terminal coverage state; unique versus raw counts; per-job detail coverage; equipment property isolation; inspected versus unavailable media; redaction checks; and `write_operations: 0`. A synthetic fixture pass validates contracts, not HCP authentication, endpoint support, or live completeness. This package's editorial choices and non-portable exclusions are documented in [Source decisions](references/source-decisions.md).

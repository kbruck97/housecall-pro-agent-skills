# Canonical story package and optional publisher boundary

## Role separation

- Strategist: selects tenant, objectives, source facts, useful angles and outcome measures.
- Studio: drafts/adapts/renders and performs internal QA, without account credentials or public authority.
- Publisher: a separately commissioned narrow executor; cannot rewrite copy, select a different target or manufacture missing evidence.

A working authoring runtime is not an authenticated channel integration; authenticated integration is not publication approval. Tenant directories alone are soft isolation; contracts may require separate credentials/processes. Never persist unrelated account discovery data under a tenant.

## Package schema

The example is synthetic and blocked. References are logical private artifact keys, not real records or external URLs.

```yaml
schema_version: 1
tenant_ref: synthetic-tenant
package_ref: synthetic-package
state: rights_pending
posting_enabled: false
integration_status: not_configured
job:
  ref: synthetic-completed-job
  completion_evidence_ref: synthetic-completion-snapshot
  scope: documented_inspection
  observed_at: null # required timestamp for actual evidence
story:
  angle: explaining_a_documented_check
  geography_precision: approved_service_area_only
  authenticity: real_job_source_required_no_reconstructed_proof
claims:
  - text: "A documented inspection included a pressure check."
    evidence_refs: [synthetic-tech-note, synthetic-image]
    limitations: no_performance_or_savings_claim
    expires_at: null # reviewer must establish applicability/expiry
    status: supported_in_fixture
media:
  - asset_ref: synthetic-image
    class: proof
    source_hash: null
    derivative_hash: null
    transform_recipe_ref: null
    visual_review: pending
rights:
  consent_refs: []
  permitted_channels: []
  revocation_checked_at: null
  state: unknown
privacy:
  pii_review: pending
  metadata_stripped: false
  redaction_evidence_refs: []
variants:
  - channel: proposed_channel
    target_ref: null
    copy: "A closer look at one documented inspection step."
    media_refs: [synthetic-image]
    alt_text: draft_requires_visual_review
    cta_ref: null
    disclosures: []
payload_hash: null
qa:
  status: blocked
  reasons: [rights_unknown, visual_review_pending, target_unbound]
approval: null
publish_receipt: null
```

In real private packages, bind each source to tenant/job/property, exact observation time and authorized locator; use a media digest rather than retaining signed URLs in public artifacts. Keep public payload free of internal IDs/receipts/PII. Consent and approval are separate: approval cannot cure absent rights.

QA must check schema/types, required evidence, supported claims and expiry, consent scope/revocation, PII and redaction review, forbidden phrases, channel constraints, exact target, metadata/disclosures, actual output readability and content/media hashes. If a validator is unavailable, label manual review and unresolved checks rather than asserting deterministic QA passed.

## Capability discovery worksheet

For each real adapter, capture binding/schema/version, official policy reference and checked date, tenant/account ownership proof, allowed operations, permissions/auth lifecycle, quota, retention, idempotency, lookup/readback support, error semantics and tests. Missing capability is `unavailable`, never an invented endpoint. Public upload, publish, comments, analytics and readback are separate capabilities. Browser access does not imply authorized unattended publishing.

HCP evidence collection remains read-only. Optional internal/private HCP surfaces require their own explicit authorization and support labels. Rendering is local by default; any remote creative/media service needs a data-disclosure/rights review first.

## Optional later release protocol

This is a design contract, not authorization to execute it:

1. Validate immutable payload and media plus source/rights freshness. A negative release test must reject an ordinary draft.
2. Verify exact account/resource ownership and tenant-specific credential context. Current official channel policy can require interactive selection, express consent, review/audit or retention limits; do not inherit stale platform tables.
3. Obtain an approval envelope binding tenant, package, payload/media hashes, exact channel and resource, final schedule/timezone, approver identity, issue/expiry and single-use approval key. A calendar approval is insufficient.
4. Atomically reserve/consume the operation through an append-only durable approval ledger. Editable `approved: true` fields are not authority or replay protection.
5. Preflight all gates again, then use verified provider lookup/idempotency to find an existing operation before one create. Never alter approved content.
6. Read the exact returned object from the provider and compare content/media/target and visibility/schedule state with approval. A scheduled object is not yet public; an accepted request is not verified publication.
7. Persist receipt, readback evidence and approval consumption. Stop on ambiguous create or receipt-persistence failure; reconcile using the same operation identity, never create again blindly.
8. For a supervised canary, stop after one object for receipt review. Expand only under separate scope approval.

A receipt binds operation key, target, payload/media hashes, provider object reference, current state, readback time/result and approval key. If a provider cannot support reliable reconciliation/readback, leave the channel manual/unavailable rather than claim publish-once safety.

Consent revocation blocks unsent derivatives immediately and invalidates stale approvals. For already published content, create an authorized takedown-review request tied to exact objects; do not silently delete or keep reposting. A complaint/public interaction is a separate human-routed workflow, not a studio-authorized reply. Never argue, diagnose, disclose the customer relationship, admit liability, promise refunds or remove criticism merely because it is negative.

## Handoff report

State scanned candidates, accepted draft candidates, skipped, blocked and reasons using one denominator. List each draft's private evidence refs and claim, selected angle, media class, rights/privacy/visual QA state and unresolved approval gates. Separate `drafted`, `QA_passed`, `approved`, `published_unverified`, and `published_verified`. Report booked leads/revenue only with attribution evidence; never invent marketing performance from the existence of posts.

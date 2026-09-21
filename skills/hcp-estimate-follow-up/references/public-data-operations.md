# Public estimate and option operations

Sources: https://docs.housecallpro.com/docs/housecall-public-api/e430ba3d520a0-get-estimates and https://docs.housecallpro.com/docs/housecall-public-api/06ba3d648e345-changelog. Discovery snapshot attribution: 2026-09-21; not live tenant verification. Expanded sidebar proves listed operation families, not unextracted payload schemas.

## Collection and state

Collect every estimate page; bind company/customer/property and exact estimate and option IDs. Record option version/line items, selected alternatives, totals, tax/discount, currency, expiration and state where returned. Do not apply all alternatives as cumulative work. Unknown fields stay unknown. Read current option state again immediately before approval, decline, conversion or revision.

Public support includes estimate list/create/get; option creation; option attachment/link/note creation and note deletion; option schedule update; option line-item listing/bulk update; and approve/decline. Upload attachments as schema-supported local binary files, not arbitrary remote URL bodies. Fetch exact endpoint schemas before execution—this reference deliberately does not fabricate payloads.

## Approval and revision procedure

1. Record the authorized customer/operator statement and its precise option/version scope. “Looks good, what dates?” is not automatically permission to approve every option.
2. Public `POST /estimates/options/approve` and `POST /estimates/options/decline` exist. Use the current documented payload, exact IDs and separate write authority. Older internal-only guidance is superseded only for documented operations, not all estimate actions.
3. `approval_status_updated_at` is the last status transition, **not approved-at**. It can change on decline and become null when status is cleared. A report must pair it with current approval state; do not calculate sales timing from it without transition history.
4. For bulk line-item replacement, capture the complete before-list and approved after-list including IDs, quantities, prices, tax and ordering as supported. Preserve unrelated items; no blind replacement from a partial page or customer prose. Revision invalidates stale acceptance assumptions.
5. Submit once and read back the exact option fields. Ambiguous timeout blocks retry until dedupe/reconciliation establishes outcome. Approval, conversion and booking are different receipts. Do not claim any undocumented public conversion path merely because a private runtime offers it.

Positive: authorized approval of selected Option A verified on that option; Option B unchanged and scheduling unresolved. Negative: treating a nonnull transition timestamp as proof of approval after the option was declined.

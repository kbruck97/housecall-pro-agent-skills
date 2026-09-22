---
name: hcp-pricebook-procurement
description: Use when reviewing HCP catalogs and draft BOMs. Separate documented pricebook operations from procurement release authority.
license: MIT
version: 1.2.0
---

# HCP pricebook and procurement readiness

Read foundations (dependency skill `hcp-foundations`). This workflow audits evidence and drafts a bill of materials (BOM); it does not place orders. See the [ledger](references/capabilities.json) for official source URLs and evidence detail.

## Capability boundary

The official pricebook overview documents materials and material-category index/create/update/delete, and price-form index/create/show/update/delete. The changelog documents service reads and expansions `expand[]=service_materials` and `expand[]=service_labor_rates`. Without expansion those lists default empty: do not report “no BOM” from an unexpanded response. The overview specifies an organization-specific API key. Exact individual method/path/body schemas must be resolved before enabling writes; operation-family coverage is not permission to invent CRUD paths.

Internal estimate templates and richer catalog observations are separate, tenant-specific adapter capabilities. FI inference is not an originating template ID. No supported public inventory-stock control, supplier purchasing, PO issuance, receiving, or automatic substitutions were established.

## Read-only readiness procedure

1. Define company, catalog scope, bounded executed-work cohort, and report date range. Use a GET-only adapter and complete documented pagination; if internal catalog traversal is separately permitted, dedupe category/resource identities and track every subtree's coverage.
2. Collect material/service identifiers, descriptions, source links, part numbers, unit/cost fields actually exposed, and expanded material/labor associations. Missing fields stay unknown. Do not confuse selling price with purchasing cost.
3. Resolve each source job and approved estimate option exactly. Bare numeric job references must be resolved, not guessed. Preserve approval state and note that `approval_status_updated_at` is not approved-at. Do not approve an option to obtain a usable BOM.
4. Classify each non-tax/non-discount line: current direct material reference; stale/missing material reference; service with one nonempty BOM; ambiguous/empty service BOM; service without mapping; freeform line. Report denominators and exclusions.
5. For each service, compare material-ID/quantity multisets across all authorized templates. Exactly one nonempty set is necessary for service-only mapping; multiple sets mean `NEEDS_REVIEW`. Template-signature matches are heuristics, not provenance. Source-prefix typing observations are adapter-specific, not a substitute for an authoritative catalog join.
6. Compare with completed-job line items and notes to identify substitutions and omissions. Repeated invoice line groups may be billing allocations, not extra equipment. Missing invoice pricebook links make invoices unsuitable as primary BOM identity evidence.
7. Build a **DRAFT / DO NOT RELEASE** output with exact supported material identities, quantity evidence, purchasing units, assumptions, site-variable ledger, and unresolved supplier questions. Separate labor, subcontractor-supplied items, measured accessories, and allowances. Do not infer universal supplier scope from another job family.
8. Gate release on current vendor SKU/pricing, pack conversions, approved substitutions, measured quantities, site/code requirements, versioned BOM and human approval. Actual PO transport belongs to a separate supported procurement adapter with its own approval and receipt/readback.

## Catalog changes

For a specifically approved correction, snapshot current affected records, calculate exact field diffs and dependent usage, and present destructive/bulk impact. Prefer proposed versioned archetypes over rewriting historical templates. Verify the individual public schema and tenant entitlement; submit only the approved patch and read back all affected targets. A material delete can break historical/current references. No create/delete probes or automatic cleanup.

## Examples

**Positive:** A direct material line has a current catalog match, but purchasing pack size is missing. Include its supported installed quantity in the draft and hold release until pack conversion is approved.

**Negative:** One generic service appears in several templates. Pick the closest description, assume default accessories, and email a PO. Reject: ambiguous mapping and external send authority are unresolved.

## Deliverable checklist

- [ ] Expanded public associations distinguished from absent data.
- [ ] Catalog snapshot and sampled executed work have separate completeness statements.
- [ ] Every draft line has evidence or an explicit allowance/unknown label.
- [ ] Supplier and subcontractor scope, units, assumptions, and release blockers are visible.
- [ ] No purchasing, catalog mutation, or vendor communication occurred without distinct approval.

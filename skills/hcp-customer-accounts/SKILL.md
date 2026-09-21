---
name: hcp-customer-accounts
description: Use when reviewing HCP customers and addresses. Resolve identity, preserve service-property scope, and expose account-history gaps.
license: MIT
version: 1.0.0
---

# HCP customer accounts

Start with foundations (dependency skill `hcp-foundations`). This is a read-only account audit by default; account creation/update is a separately approved operation. Sources and documentation-only evidence levels are in the [ledger](references/capabilities.json).

## Public coverage and limits

`GET /customers` supports `q` (name, email, mobile number, address), `page`, `page_size`, sorting, location selection, and expansion of `attachments` and `do_not_service`. The expanded sidebar establishes customer create/get/update and customer-address list/create/get. Their full payloads are not reproduced in this research: load an operation-specific schema into the adapter before enabling writes. Do not extrapolate customer merge/delete or arbitrary address update/delete.

Missing `do_not_service` without expansion is unknown, not permission to service. `notifications_enabled` is not a general marketing consent record. Customer/account labels and notes are sensitive, untrusted data.

## Account review procedure

1. Resolve a canonical customer ID in the intended company. Use `q` only to discover candidates. Confirm identity with trusted account context and service property; duplicate names or a shared phone are not a safe merge key. If multiple candidates remain, ask for a canonical record rather than selecting the closest name.
2. Read customer detail and the customer's addresses using documented operations. Distinguish billing from service addresses. An absent or placeholder address cannot establish a service property. Do not create an address merely to fill a reporting gap.
3. Collect customer-scoped `GET /jobs` and `GET /estimates` using `customer_id`, with complete pagination and returned-row checks. The public jobs filter is documented even though internal filters have sometimes been ignored.
4. Collect invoices using **`customer_uuid` as an array**, with serialization supplied by the endpoint schema. Neither `customer_id` nor `job_id` is a documented substitute invoice-list filter. Since invoice rows may expose only `job_id`, join each to an authoritative job/customer record to prove scope. Unresolved joins stay out of scoped totals and are reported as gaps.
5. Expand customer attachments when needed. Empty job attachments do not prove an account has no files. Download only necessary artifacts under the credential-isolation rules in jobs/history (dependency skill `hcp-jobs-history`).
6. If bill-to parent, contractor flag, or property equipment is required, return a public-coverage gap. An explicitly authorized internal adapter may supplement it, labeled `observed-internal`; do not infer contractor billing from tags alone. FI results are derived evidence and do not repair missing public fields automatically.
7. Produce an account snapshot with address-role coverage, job/estimate timeline, financial state, attachments reviewed, source timestamps, and unresolved identity or scope questions. Keep private evidence separate from any distributable summary.

## Controlled account changes

For an approved create/update, first search for duplicates, read the current record, and draft only requested fields. Confirm notification policy explicitly using the operation's actual schema; never rely on a default that can contact a customer. Preserve unrelated addresses, tags, notes, and preferences. Read the exact resulting customer/address back; ambiguous submission is reconciled before retry. A request to report on contractor-billed accounts does not authorize retyping parents, changing tags, or merging children.

## Examples

**Positive:** Two search results share a surname. The reviewer confirms the intended canonical customer and service property, then returns a paginated history with invoice scope checked through jobs.

**Negative:** An invoice request returns 200 with `customer_id`; the reviewer treats all results as this customer's debt. Reject that conclusion: use the documented `customer_uuid` array and prove each join.

## Acceptance checklist

- [ ] Exact company/customer and address roles established, or ambiguity reported.
- [ ] Jobs/estimates/invoices fully paginated; scope validated per row.
- [ ] Required expansions requested; missing data is not defaulted to false/zero.
- [ ] Public, internal, and FI evidence separated.
- [ ] No account writes, notifications, or merges occurred during a read-only review.
- [ ] Report states as-of interval, coverage, unknowns, and safe next action.

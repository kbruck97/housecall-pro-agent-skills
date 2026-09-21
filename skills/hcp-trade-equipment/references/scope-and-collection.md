# Scope and collection contract

## Capability surfaces

| Surface | Purpose | Preconditions | Forbidden inference |
|---|---|---|---|
| Documented public adapter | Jobs, customers, addresses and other currently supported reads | Tenant authorization plus endpoint-specific capability verification | One working job GET proves every endpoint works |
| Optional private alpha/React adapter | Evidence omitted by public reads, property inventory, approved equipment writes | Explicit opt-in, authenticated tenant-isolated session, observed response contract | Private routes are supported public APIs |
| Optional secondary inventory adapter | Identity pairs, guarded plans and local inventory state | Configured adapter and separate authority | Its IDs are HCP IDs or actions are universally installed tools |

Probe only harmless authorized reads. Cache method, route template, status, response shape, scope validation and limitations; omit credentials and signed URLs. A public key may expose a subset of private-shaped reads in some installations, but that is not a portable contract. When private equipment access expires, refresh through the secure auth adapter once and retry the original read once. If still blocked, stop dedupe/writes. Repeated fresh logins can invalidate MFA challenges and cause lockouts. Never mix tenant session state.

Historical private route templates to validate, not guarantees:

- `GET /alpha/jobs/{job}` and its `line_items`, `notes`, `attachments` collections.
- `GET /alpha/customers/{customer}` and customer attachment collection.
- `GET /alpha/equipment/types`, paginated equipment collection, equipment detail, and equipment `service_requests` collection.

A 200 must be parsed and scope-checked. A 401 is unavailable authorization, not empty inventory. A 404 might indicate an unsupported route or unresolved identifier; it does not prove entity absence. Use bounded backoff for transient rate limits and record final coverage separately from failed attempts.

## Service-address resolution

Inspect `address_id`, `service_address_id`, `service_address.id`, `address.id`, and `address.data.id`. These are alternative payload shapes, not interchangeable answers: if multiple nonempty values disagree, stop for scope review. Reject an identifier whose payload is the provider's all-zero address sentinel. Do not publish a sentinel as a real example ID.

A non-null identifier is necessary but not sufficient. Resolve it to a real service property owned by the intended customer. Billing-only records and company-name-only printable labels do not establish work location. Coordinates and timezone are useful context, not mandatory truth predicates; absence alone does not invalidate a documented service property.

A null job address differs from an explicit no-address sentinel. Null can be recoverable when an authorized private comparison of street, city, region and unit fields yields exactly one actual service address on the same customer. Record the recovery evidence and unlinked-job data-quality issue. Ambiguous matches, missing unit information or multiple plausible properties block recovery. Do not change the job's address as an incidental side effect.

## Inventory scope and completeness

1. Try the configured property query, then validate every returned row's property and customer relationship.
2. Empty or mixed results can reflect ignored filters. If authorized for broader reads, enumerate the full supported list, paginate to exhaustion and filter locally. Otherwise mark scope incomplete and stop creation.
3. Follow actual pagination metadata, checking repeated cursors/pages and duplicate row IDs. An arbitrary page cap is a partial scan. Reconcile declared totals with collected unique rows.
4. Customer-level inventory spans properties. Group by service-address key; never merge same-model units from different properties.
5. Equipment-linked jobs and embedded customer job lists are discovery leads. Fetch exact jobs and prove customer/property membership before attributing work. A recent global job feed is not complete customer history.
6. Parse response containers deliberately. Historical shapes include `data` arrays and `data.data` arrays. Do not iterate object keys as evidence rows or recursively flatten arbitrary nested objects into attachments.

## Attachments

Record stable private artifact keys, source job/customer relationship, media type, retrieval status, content hash and reviewed component. Filenames and free-text names may contain personal data. Customer-level registration documents can exist when every job attachment list is empty; include them but do not invent their job relationship.

Download third-party signed media with a fresh unauthenticated client. Do not forward HCP cookies or authorization across origins, including redirects. Use the authenticated client only for an explicitly trusted same-origin resource. Do not log/persist signed URLs. On expiry, refresh authorized metadata rather than treating the attachment as absent. Retain private originals under the operator's retention policy; publish only approved redacted derivatives.

Empty lists, thumbnails, oversized skips, unsupported videos, unreadable documents and actual inspected media are distinct coverage states. A logo/map/avatar is not equipment evidence. Never infer photo-to-artifact identity from contact-sheet position.

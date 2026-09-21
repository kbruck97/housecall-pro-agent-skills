# Adapter contract and bounded collection

## Support tiers

| Surface | Allowed default use | Required guard | Not a guarantee |
|---|---|---|---|
| Public | Authorized job/customer evidence collection | Tenant-scoped secure credential binding and endpoint-specific capability check | Public evidence includes equipment, private notes, or all media |
| Private alpha | Opt-in reads for missing evidence and equipment inventory | Explicit private-surface approval, supported session adapter, exact tenant/object check | Historical paths and payloads still work |
| Private React | Opt-in supplemental structured job/segment/media metadata | Same scope as alpha, schema check before interpretation | Every embedded URL is an attachment |
| Optional local equipment store | Separately authorized comparison | Store identity, freshness, source mapping | An empty mirror proves live HCP is empty |

Public and private refer to API surface, not whether customer data is public. All business records remain restricted. A public token working on one private path does not authorize or prove support for other private paths. Do not move a credential between origins to test guesses.

No function names below are available tools. Integrators must bind real tools to these **logical capabilities**, document the binding, and test it independently:

- Read exact customer/job and declared relationship fields.
- Enumerate customer jobs, service addresses, and property equipment.
- Read job line items, notes, attachment inventory, and equipment detail/job relationships.
- Optionally read expanded attachments, customer attachments, estimate options, or composite segments.
- Optionally refresh a private session without revealing its secrets.

### Adapter declaration

| Field | Type / rule |
|---|---|
| `adapter_alias` | Non-sensitive local label |
| `surface` | `public`, `private_alpha`, `private_react`, `local_mirror` |
| `read_only` | Must be true for this workflow |
| `capabilities` | List of logical capabilities with actual integration bindings kept private |
| `approval_ref` | Opaque approval alias; required for every private surface |
| `tenant_guard` | Method that confirms the active account and exact object ownership |
| `id_formats` | Per-object validation rules from the actual integration contract |
| `envelopes` | Per-capability allowed row paths and metadata paths |
| `pagination` | Cursor/page scheme, start, next/terminal rule, page-size bound, total scope |
| `retry_policy` | Maximum attempts and duration; authentication refresh bound |
| `attachment_policy` | Origin allowlist, redirect validation, MIME and byte limits |
| `snapshot_policy` | Time boundary, stable-order support, staleness tolerances |

Configure actual endpoints and origin names outside the distributable package. Do not claim support simply because a guessed route returns HTTP 200: HTML login pages and ignored filters can do that too.

## Envelope normalization

Use capability-specific row paths, not “recursively find any list.” Examples of allowed shapes after adapter validation:

```json
{"jobs":[{"id":"job_A","customer":"customer_A"}],"total_items":1,"total_pages":1}
```

```json
{"data":{"object":"list","data":[{"id":"equipment_A","property":"property_A"}]},"total_count":1,"total_page_count":1}
```

All identifiers in examples are deliberately synthetic aliases, not executable provider IDs. A list of response pages is not a list of records. Keep outer pagination metadata while extracting only the declared inner row list. Unknown shape must raise a collection error; returning an empty list hides defects. Require each row to be an object with a valid stable identity and explicit scope evidence.

For React line items, normalize declared `material_line_items` and `labor_line_items` separately, retain category and source-item alias, then concatenate for review. Do not infer equipment count from container keys.

## Pagination and filter proof

1. Read each page once in the declared traversal; retain seen cursors and identity sets.
2. Compare raw and unique counts and quarantine out-of-scope rows. A requested filter is not a scope proof.
3. If totals describe the whole tenant, do not compare them to customer-filtered counts. Store `total_scope` explicitly and verify the collected set for that same scope.
4. Repeated cursors or identical pages with `has_more` true indicate failure. Stop at a configured page/time budget; report partial rather than silently truncating.
5. A stable total and equal raw count are insufficient if IDs repeat. If the adapter supports stable sorts and the scope authorizes a full inventory, collect bounded alternate-order passes, union by stable ID, and require unchanged totals and matching unique coverage. Unknown sort parameters must not be guessed.
6. Even an equal union is a bounded observation, not transactional snapshot proof. Concurrent changes, divergent detail payloads, or inconsistent totals require a fresh boundary or a partial receipt. Never drive “missing-source” retirement from partial discovery.
7. If a filter is ignored, use a verified alternate scoped capability. A full-list/local-filter fallback requires separate broader-read authorization and minimum retention; otherwise stop. Do not crawl all customers to compensate for one failure.

## Failure recovery

- `401`: do not assume merely expired cookies. Verify binding; allow one authorized refresh and one replay. Repeated failure stops that surface.
- `403`: report permission/setup denial; do not switch accounts to evade it.
- `404`: distinguish exact-object miss, unsupported capability, and wrong tenant. Only approved alternate capabilities can clarify; absence is not established.
- `429` or transient server failure: obey available retry guidance within configured attempts/time. Record final outcome separately from transient attempts.
- Browser collector timeout: a preconfigured direct HTTP adapter may reuse the same tenant-bound authentication context. Do not export cookies to ad hoc scripts or weaken scope/transport policy.
- Success without JSON or required identity: contract failure, not empty success.

## Attachment security

Authenticated metadata reads and file downloads are separate clients. A signed third-party download uses a fresh unauthenticated client with no business-system Authorization/Cookie headers; validate redirects at every hop and never forward credentials across origins. Trusted-origin requests still need scoped authentication. Reject unapproved schemes, local/private-network targets, and oversized responses under the configured fetch policy.

Fetch promptly after metadata discovery. On expiry, refresh metadata once through the authorized capability; otherwise record `expired_uninspected`. Verify MIME by decoding/signature rather than filename. Deduplicate identical bytes without discarding attachment-to-job provenance. Never persist signed URLs, request headers, or raw session state in evidence bundles.

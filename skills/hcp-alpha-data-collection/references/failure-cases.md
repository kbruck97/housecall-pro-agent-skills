# Synthetic failure and acceptance cases

All cases are invented. Execute these against a real adapter's offline test harness before enabling it. This package does not claim to supply that harness.

| Input / condition | Required result | Forbidden shortcut |
|---|---|---|
| Public body has `jobs` list, total 1 | Parse one row and verify ownership | Reuse data-only parser and return empty |
| Nested `data.data` equipment list is empty, outer page wrapper is a one-element list | Zero records after successful terminal proof | Count the wrapper as equipment |
| Total 3, page rows A/B/B | Unique count 2; partial | Declare complete from raw count 3 |
| Totals drift from 3 to 4 between passes | New boundary or partial | Union and mark transactional completeness |
| Customer filter returns rows for customer_B | Quarantine; alternate scoped read or approved wider scan | Follow customer_B addresses/media |
| Private equipment 401, public job succeeds | One bounded private refresh; block equipment dedupe if still unavailable | Treat public job success as zero equipment |
| Missing attachment route but supported expansion returns a PDF | Inventory one metadata-only item | “No attachments” |
| Attachment metadata has only endpoint self-link | No file entry | Fetch self-link as photo |
| Three downloaded images are logo/avatar/map pin | Inventory classified UI artifacts, no plate assertions | Three equipment photos |
| One image duplicated in alpha and React | One media content item retaining both relationships | Two physical units |
| Valid session belongs to other tenant | Stop scope branch | Interpret clean 404 as absent customer |
| Canceled proposal appears only in public list | Union discovery, exact detail review, proposal classification | Installation from paid deposit |
| Composite job references sibling segment | Collect only declared, verified sibling relationship within scope | Recursively scrape arbitrary identifiers |
| Customer attachment has unit plate but no job link | Customer-level presence/identity only | Attribute installation to nearest job |
| Request requires nameplate-only evidence, only registration exists | Report plate coverage unmet | Label registration visually verified plate |
| Signed download redirects outside trusted origin | Fresh unauthenticated client plus redirect policy | Forward authenticated headers |
| Required envelope unknown with HTTP 200 | Contract failure; no zero defaults | Empty collection |

## Worked miniature

The requested customer is customer_A with property_A. Public lists job_A and job_B; private alpha lists only job_A. Exact job_B detail confirms the same customer but contains a canceled proposal. Job_A detail confirms completed boiler maintenance. Equipment reads are unavailable. The correct bundle contains two reviewed jobs, one performed-work observation, one proposal observation, and unavailable equipment coverage. Downstream review may propose one serviced-existing physical boiler with unknown identity; it must not claim a newly installed boiler or safe-to-create missing equipment.

## Acceptance checklist

- Every collection branch has a terminal or explicit failure state.
- Unknown wrappers and ignored filters cannot become successful empty results.
- All exported evidence aliases resolve locally without exposing the private mapping.
- Totals are checked against the correct population and deduplicated identities.
- Surface parity and media inspection are separate checks.
- Credential-bearing downloads never share a cross-origin authenticated client.
- A receipt cannot say complete when a required branch is unavailable.

# Decision rules and failure modes

## Evaluate different claims with different evidence

There is no global ranking that makes every field on a stronger-looking source true.

| Claim | Strong evidence | Insufficient evidence |
|---|---|---|
| Unit exists | Target-bound plate/photo, explicit completed service/install narrative, tied maintenance worksheet | Brochure artwork, appliance-named closet, unaccepted proposal |
| Job installed unit | Performed-install scope plus completion and property/unit tie | Paid invoice alone, existing inventory, post-work photo alone |
| Job serviced unit | Named-unit diagnosis/maintenance/repair and performed-work evidence | Intake request, future evaluation, unrelated room photo |
| Exact model/serial | Target plate; matched registration/worksheet only in document-enabled mode | Sibling plate, inferred model family, generic manual |
| Technology/class | Exact installed-model documentation, explicit plate class, performed scope | Color, cabinet shape, multistage thermostat capability |
| Installation date | Explicit installed-date evidence; labeled completion proxy only if permitted | Service date, import timestamp, serial manufacture code, approximate age |
| Unit count | Distinct physical identities and context, explicit unit counts in performed scope | Attachment count, consumable quantity, labor quantity, repeated invoice groups |

A finished job plus “replace later” remains proposed replacement. A customer-installed system commissioned by the contractor is serviced-existing, not installed-new by that contractor. Preserve attribution independently of equipment existence.

## Cardinality algorithm

1. Partition evidence by property, physical role, time period, and target context.
2. Group identical full-serial views of the same role/property. Check if a number is actually a component serial or duplicate copied record before merging.
3. Treat different full serials as different units only when target context supports it. Conflicting rows on one plate or two dates on one replacement history require adjudication.
4. Reconcile physical identities with performed-scope counts. Keep explicit scope count and observed count separate when they disagree.
5. Do not allocate unknown side/room mappings. Two generic furnaces can be numbered for bookkeeping without asserting their locations.
6. Preserve replacement chronology: an old removed unit and a new installed unit are not two simultaneously current units. Without removal evidence, hold current-state classification rather than delete the older record.

## Component boundaries

- A furnace blower motor, ignition component, filter drier, and refrigerant charge are repair detail, not separate appliances.
- An evaporator coil and outdoor condenser may be tracked separately if policy requires it and both are independently evidenced. A photo of filters does not establish indoor head count.
- A combination boiler with domestic-hot-water function is one cabinet, not both a boiler row and tankless-water-heater row for the same unit.
- Generic “all necessary controls and pumps” does not prove counts or installed accessories. Explicitly replaced controllers/sensors can be event rows only under an accessory-event policy. Do not elevate them to standalone inventory by enum membership.
- Source/load loop pump readings do not establish independent pump assets. Clear independently serviceable zone circulators can qualify only under the active fleet policy, with identity unknown if unreadable.
- A replaced switch without a named recipient supports only the accessory event when allowed; do not borrow a parent from a plausible existing inventory record.
- “Other” means a positively identified permitted durable class lacking a named enum. It is not a fallback for “some equipment.”

## Adapter and media safeguards

Use an approved public collector for documented reads it actually supports. Private alpha/React parity can add evidence only after opt-in and tenant validation. Neither a private path nor a historical successful call is a present-day capability guarantee. Optional private inventory stores are additional evidence surfaces, not public HCP endpoints.

Inspect dedicated attachment containers. UI avatars, map icons, organization logos and chat links are not job attachments. Preserve real originals even when their filenames suggest thumbnails or have no extension; MIME and decoded content matter more than names. Missing originals, oversize limits, expired links and unsupported formats are coverage gaps.

When live downloads are separately authorized, do not forward service authentication to third-party media origins. Use a fresh unauthenticated client for signed media links; validate redirects and allowed destinations. Keep signed links and raw filenames out of published evidence. The adjudicator consumes inspected artifacts and does not need credential material.

## Failure-to-action table

| Failure | Required action |
|---|---|
| Expanded line items absent | Check dedicated authorized collection; mark missing until hydrated |
| Claimed omitted photos exceed provider inventory | Compare authorized inventories and declared totals; do not fabricate missing photos |
| Quantity two on ductwork plus one HRV photo | One observed HRV at most; no two-unit installation claim |
| Manual lists several capacities | Leave exact capacity unknown; do not choose the largest variant |
| Live equipment query ignores property filter | Validate rows and use authorized scoped pagination/local filtering; do not widen data collection without permission |
| Dedupe snapshot predates another review | Refresh before actionable recommendation; leave not-assessed if unavailable |
| Identical model at two properties | Do not merge; property identity is a hard boundary |
| Boiler service documented but no identity | Include generic serviced boiler in permissive inventory; hold under identity-required creation policy |
| No allowed classes after complete collection | Empty result with exclusion receipt, not “no equipment exists” |
| Incomplete history | Partial result; no exhaustive absence claim |

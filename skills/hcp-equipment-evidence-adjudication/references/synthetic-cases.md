# Synthetic acceptance cases

All labels and assertions below are invented. They are editorial test vectors, not observations from a tenant and not API responses. Execute these as review checks before adopting a local serializer or decision implementation.

| Case | Input facts | Expected decision | Forbidden shortcut |
|---|---|---|---|
| A | Complete job explicitly installed two furnaces; two distinct plate serials; repeated third photo | Two installed-new units; duplicate photo ignored | Three units from three images |
| B | Quantity-two ductwork bundle for ventilation; one ventilator in room photo | At most one observed-existing ventilator if policy permits; install date null | Two installed ventilators |
| C | Completed commissioning of customer-installed ductless system; outdoor targeted only | One serviced-existing supported unit/system; no inferred head | Contractor installed the system |
| D | Generic labor quantity one; performed note names two furnaces and one boiler | Three serviced candidates if allowed; unknown identities/location mappings retained | Use labor quantity as total unit count |
| E | Completed repair replaced furnace motor and explicitly installed controller; accessory mode enabled | Serviced furnace plus foldable controller event; no motor asset | Motor becomes air handler |
| F | Single combination boiler plate and dual heating/DHW description | One asset with secondary function | Duplicate boiler and tankless rows |
| G | Proposed coil replacement after completed cooling diagnostic | Serviced cooling unit; coil recommendation excluded from installed-new | Completion performs the recommendation |
| H | Manual plus explicit installation of model family; no exact variant | Generic installed class/family only in permissive mode; identity gate hold if required | Brochure variant chosen as installed model |
| I | Heater closet piping only; no direct appliance presence | No heater candidate | Room name proves appliance |
| J | Completed water treatment installation; policy excludes that class but enum includes it | Excluded, no row | Use enum membership to override scope |
| K | Alpha and React copies have identical bytes; UI has extra avatar | One artifact; avatar excluded | Three independent photo witnesses |
| L | Attachment access denied and other sources incomplete | Partial/blocked receipt, not complete empty inventory | Treat denied as zero |
| M | Same-model records at property; no serial/location tie | Ambiguous dedupe, no write recommendation | Merge by model alone |
| N | A later pass already created matching serial at same property | Refreshed match recommendation, not new | Trust earlier no-match snapshot |
| O | Paid import timestamp differs from historical finish date | Historical date for chronology; no install date for service | Import time becomes install date |
| P | Same cabinet has contradictory plate/registration serials | Preserve conflict and target-source precedence; review if binding unresolved | Split into two units automatically |

## Receipt walkthrough

For case C, suppose scope is verified, a completed commissioning note is inspected, attachment enumeration is complete and empty, and dedupe is not requested. Expected receipt values are: mode `serviced_existing`, one candidate considered and included, zero held/excluded, install-date check pass because null, dedupe check `not_run`, remote writes zero, and result `complete_read_only`. “Complete” refers to the supplied review scope, not proof of a full property inventory.

For case L, output may contain supported partial candidates, but the coverage check cannot pass as exhaustive. Specify which source is unavailable and which assertion it blocks. A strict array-only output must not silently conceal that limitation; negotiate a sidecar or return a supported blocker format.

# Synthetic acceptance cases

All aliases and product strings here are invented. These are offline policy tests, not live-system verification.

| Input fixture | Expected plan and receipt | Failure to catch |
|---|---|---|
| CARD-A and ROW-A linked at PROPERTY-A; one maintenance job | One physical unit, two claims, no new records; installation date stays null. | Counting stores as units or dating installation from service. |
| Completed evaluation explicitly lists two furnaces; no cards and no identity fields | In serviced-existing mode, two anonymous units may be proposed if quantity denotes physical units and dedup coverage is complete. In installed-new mode, no installation claim. | Universal make/model gate suppressing valid existing inventory, or service being labeled installation. |
| One new unit approved for both stores, both creates verified | units_seen 1, created calls 2, by-store creates 1 each; matched 0 if no pre-existing record. | Reporting two units or one write. |
| Same card updated twice successfully, both readbacks equal requested fields | updated calls 2, distinct updated records 1; only one physical unit. | Deduplicating writer-call totals. |
| Two same-model units have different legible serials | Keep separate labels and records. | Model-only merge. |
| Same broad type at PROPERTY-B; source job at PROPERTY-A | Leave PROPERTY-B unchanged; no cross-property reassignment without proof. | Customer-level scope treated as a property match. |
| Complete job contains only complaint notes | No new installed unit; evidence gap stated. | Completion status treated as installation proof. |
| Cartridge plus filter-change labor | Service durable housing; no cartridge asset. | Every line item becomes equipment. |
| Linked pair has contradictory model text but established same-unit service history | Preserve disputed field, report needed nameplate evidence; identity and field uncertainty separate. | Duplicate creation or blind overwrite. |
| Legacy water-heater type with no decisive plate/model/photo | Keep coarse type; list tank and tankless candidates. | Guessing canonical type from display name. |
| Accepted update drops last-service field | Successful-call ledger records acceptance; receipt flags mismatch and field unset. Approved notes may preserve dated service evidence. | Claimed field success based on response status. |
| HCP create succeeds, FI create times out | Partial pair; exact HCP readback; reconcile FI outcome before retry. | Duplicate HCP create or false atomic success. |
| List returns mixed properties or a next-page cursor | Coverage incomplete until scoped authorized pagination finishes; block creates. | Empty/partial page interpreted as no duplicates. |
| Verification clean before final update but no later readback | applied-unverified; final fresh inventory still required. | Reusing stale verification. |

## Minimal receipt examples

A dry-run audit reports completion_state planned, write_counts all zero, proposed operations separately, and coverage limitations. It must not claim a transaction was closed by a server.

A verified paired create reports completion_state verified, units_seen 1, matched 0, successful creates 2, verified creates 2, unresolved_units 0, both exact-target comparisons true, association comparisons true, adapter_close_status accepted only if that adapter actually accepted close.

A refused model update reports successful updates 0 for that attempt, unresolved unit and model evidence needed, then verifies unchanged state. A later approved name-only update is independently counted; it does not resolve the model dispute.

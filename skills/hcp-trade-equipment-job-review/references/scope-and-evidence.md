# Scope policy and field-specific evidence

## Conservative portable taxonomy

Load a versioned policy before classifying. Preserve stricter installed tenant exclusions; never use a generic policy to override them. A policy change is explicit, versioned, and approved outside an individual extraction. It is not inferred from an old example or a schema's `trackable` field.

Default candidate classes are durable, separately serviceable appliances: furnaces; condensers; heat pumps including geothermal; air handlers; boilers; ductless outdoor units and documented indoor heads; HRV/ERV; humidifiers/dehumidifiers; durable air-cleaning equipment; packaged or unit heaters; tank, tankless, and indirect water heaters; and durable water-treatment stages such as softeners, filtration housings, reverse osmosis, and UV systems. Standalone hydronic/boiler zone circulators may be candidates when explicitly identified; geothermal source/load/flow-center pump components are folded into their parent system.

Retain the source's conservative equipment-profile exclusions by default: evaporator coils, thermostats, zone-control boards, dampers, sump/sewage/ejector/well/booster/domestic-recirculation pumps, pressure tanks, backflow devices, water-main/smart shutoffs, whole-home repipes, and separately tracked water-treatment control heads. Do not reintroduce these as `trackable:false` rows. Mention relevant excluded work only inside the supported parent's evidence or an exclusion count in the receipt. A hydronic zone circulator is not a domestic hot-water recirculation pump.

Electrical equipment is an optional approved trade extension: panels, generators, transfer switches, EV charging equipment, battery systems, and solar inverters may qualify with distinct-asset evidence. Service size, wire, conduit, fees, and whole-building rewiring describe infrastructure or work, not automatically physical equipment rows. Never turn a trade label into asset proof.

Consumables, labor, refrigerant added, salt/resin/cartridges, generic materials, proposals, diagnostics, and warranty transactions are not assets. Distinguish a filter housing from the cartridge it contains. A brine tank may be separately represented only when the policy and evidence establish it as a distinct tracked unit; otherwise fold it into the softener. Controls or accessories not absolutely excluded may be included only under an explicit accessory schema and never promoted to ordinary equipment by default.

### Policy schema

`policy_alias`, `version`, `approval_alias`, `allowed_trades`, `allowed_classes`, `excluded_classes`, `fold_into_parent`, `optional_accessory_classes`, `include_retired`, `identity_minimum_for_new_install_write`, `date_precision_policy`, `derived_spec_policy`.

Enforce precedence: excluded class → omit independent candidate; folded class → parent evidence only; optional accessory → emit only if explicitly requested; allowed class → evaluate evidence gates. Unknown taxonomy → hold for policy decision, not arbitrary `Other`. For existing-record mode, account for excluded records in the receipt without inventing an allowed replacement object.

## Evidence questions are independent

| Question | Strong evidence | Weak or insufficient alone |
|---|---|---|
| Does the unit exist here? | Scoped performed service, exact site photo, reliable current equipment/profile evidence | Proposal, trade tag, incidental equipment elsewhere |
| Was it installed by this job? | Unit-specific completed installation/commissioning text and corroborating docs/line items | Payment, scheduled scope, a photo of an old unit |
| Which physical identity? | Readable target-unit plate; explicit installed-product registration; unambiguous completed unit text | Brochure, accessory plate, unreadable OCR, legal manufacturer name |
| How many units? | Explicit installed/service count, distinct labels/locations/serials | Photos, invoice fractions, rooms, nominal capacity, plural wording without exact count |
| Is it current? | Later service/presence and no documented replacement; explicit current record with stated provenance | Old status alone, future replacement proposal |
| Was it serviced then? | Performed work and actual finish/service record tied to this unit | Inventory-only job linkage, billing date, profile note listing assets |

Evidence precedence is field-specific. A nameplate proves the pictured unit's identity but may document the failed predecessor; completion text can identify the new unit. A registration can establish installation identity but does not satisfy plate-only inspection. Existing equipment fields assist matching, not automatic truth; curated dates and last-service fields may be stale.

## Counting and chronology

- Ductless topology: one supported outdoor unit plus each documented head. Never infer maximum head count from outdoor model capacity. If only “heads” is stated, record count uncertainty; do not fabricate exactly two rows.
- A combi boiler supplying domestic hot water can be one physical appliance with two roles. A separate indirect tank is another appliance only when installation/presence evidence proves a physical tank.
- Internal backup heat or geothermal loop hardware stays with its parent unless approved policy explicitly distinguishes a standalone asset. Do not invent an air handler from generic “forced-air unit” wording when it describes the same heat pump.
- Fractional progress billing describes money/work allocation. Preserve all job provenance, but count physical units from actual scope. If commissioning date is absent, leave installation date unknown or use an explicitly approved labeled completion proxy; do not choose earliest/latest invoices simply to fill a field.
- Imported sections can mention other properties or third parties. Gate each relevant assertion, not just the container job. Billing-only attribution cannot establish a service property.
- A newer same-type unit does not retire an older unit unless evidence establishes replacement of that exact predecessor. Concurrent same-type units are common.

## Identity and media discipline

Inspect originals for small labels; contact sheets are triage only. Keep the exact attachment alias visible to avoid assigning the wrong plate to a unit. Record unresolved characters, not guessed ones. Component labels do not identify the parent appliance. Old-unit photos, installation photos, registration rows, and replacement order documents need explicit physical-unit assignment.

UI assets and generic PDFs cannot fill plate identity. Metadata-only files remain uninspected. No inferred make from model prefix or parent-company branding. Derived capacity/refrigerant/filter information needs a cited verified technical source and a separate `derived` basis; service refrigerant pounds are not capacity. Life expectancy is outside this package unless a versioned approved policy is supplied.

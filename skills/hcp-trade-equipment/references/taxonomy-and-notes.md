# Taxonomy, names and structured evidence

## Trackability before mapping

First decide whether the item is a durable independently tracked unit under the configured trade policy. Then map it into the current provider taxonomy. Do not let a flat provider enum turn every fitting, component, labor category or wiring project into an asset. A complete profile may retain accessory details in parent notes without creating standalone cards.

| Physical class | Mapping principle |
|---|---|
| Main panel / subpanel | Electrical-panel class; distinguish role and actual supported amperage in name/notes |
| Generator | Generator class; transfer switch separate only under policy |
| EV charger, battery, load management | Exact current class if present, otherwise approved generic mapping with precise subtype |
| Furnace / boiler / water heater / tankless | Keep functional appliance class distinct; combi appliance is not automatically two units |
| Cooling-only outdoor / reversible heat pump | Use exact model evidence, not number of zones, to decide function |
| Ductless indoor head / air handler / coil | Preserve physical component identity and system relationship; choose an approved closest class without pretending all indoor units are the same |
| ERV / HRV | Ventilation class if present; never silently relabel as heater just because a historical adapter accepted it |
| Pump / pressure tank | Distinguish pump function and passive tank; generic mapping requires explanation |
| Water softener / filtration / RO / UV | Distinguish complete treatment unit from service cartridge, valve and consumables |
| Solar array / inverter | Preserve array versus inverter distinction and trackability policy |

If no semantically acceptable class exists, retain the candidate in review. An approved `Other` category may preserve a precise name and note, but does not override the allowlist. Fetch current IDs through the configured adapter; examples deliberately contain no live taxonomy IDs.

## Naming and notes

Use a stable canonical name based on known class, make/model and distinguishing component/location. Do not include customer names, full addresses, speculative capacities or copied sibling serials. Unknown parts stay absent, not fabricated. Display names are not reliable identity keys.

Suggested evidence note structure:

```text
Evidence basis: installed-new | serviced-existing | documentary-only
Physical component: <supported role>
Capacity/Amperage: <value, units, operating condition, source or unknown>
Location: <documented unit location or unknown>
Installation date evidence: <source and confidence or unknown>
Manufacture date evidence: <separate source/inference or unknown>
Warranty: <documented scope or unknown; not a promise of coverage>
Evidence: <specific artifact and unit relationship>
Unknown: <explicit missing fields>
Conflict: <unresolved source disagreement or none>
Source job: <private runtime locator>
Tracking key: <stable scoped unit key>
Taxonomy mapping: <precise subtype, chosen category, approved lossiness>
```

The tracking key should use scoped physical identity rather than mutable display text. A model without serial is rarely globally unique. Do not create a global merge key from customer names or addresses. Keep source locators in private operational output only; public derivatives use pseudonymous artifact keys.

## Field fidelity

Retain exact plate model/serial spelling and a separate comparison normalization. Strip comparison whitespace only under documented policy; do not silently alter source identifiers. Leave unknown installation dates blank. Preserve configuration-dependent ratings and units. A warranty program's corporate family name is not the nameplate make. Field-specific provenance prevents a credible document from lending false certainty to unrelated fields.

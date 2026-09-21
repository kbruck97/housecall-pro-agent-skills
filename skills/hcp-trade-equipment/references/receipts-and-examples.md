# Receipt schema and synthetic acceptance cases

All examples are fictional tokens, not provider IDs or working API payloads. Runtime locators belong only in private evidence.

## Required receipt fields

- `schema_version`, `mode`, `tenant_key`, `property_key`, `scope_verified`.
- `coverage`: one row per required surface with `state` (`complete`, `partial`, `unavailable`, `not_requested`), unique rows, pagination exhausted, scope validated and blocker.
- `units`: stable unit key, physical class, evidence basis, fields with provenance, current-record match, unknowns/conflicts and decision.
- `operations`: planned action, approval, before-state checked, request outcome, readback result and source-job-link verification.
- `counts`: physical units reviewed, records created, records updated, existing unchanged, review units, failed operations. Refused attempts do not count as successful writes.
- `completion`: `read_only_complete`, `write_verified`, `blocked`, or `partial_failure`; remaining blockers and next evidence/action.

```json
{
  "schema_version": "1.0",
  "mode": "serviced-existing",
  "tenant_key": "tenant-synthetic",
  "property_key": "property-synthetic",
  "scope_verified": true,
  "coverage": [{"surface": "equipment", "state": "complete", "unique_rows": 0, "pagination_exhausted": true, "scope_validated": true, "blocker": null}],
  "units": [{"unit_key": "unit-A", "physical_class": "boiler", "evidence_basis": "completed maintenance line", "fields": {"model": null, "serial": null, "install_date": null}, "current_record_match": null, "unknowns": ["model", "serial", "install_date"], "conflicts": [], "decision": "propose_existing_inventory_candidate"}],
  "operations": [],
  "counts": {"physical_units_reviewed": 1, "records_created": 0, "records_updated": 0, "existing_unchanged": 0, "review_units": 1, "failed_operations": 0},
  "completion": "read_only_complete",
  "remaining": ["Creation requires approved existing-inventory policy and write plan"]
}
```

This deliberately narrow fixture shows only the equipment coverage row; a real full-job receipt also accounts for all other required collection surfaces.

## Acceptance cases

1. **Category labor only:** completed installation job, real property, no narrative/photos/identity, generic labor lines. Strict installed-new outcome: hold, no create; request installed-unit evidence.
2. **Serviced boiler:** completed boiler tune-up, quantity one, empty fully checked inventory, no make/model. Existing lane: one candidate with unknown fields, no invented installation date; read-only result does not write.
3. **Same-model siblings:** two target plates show different full synthetic serial strings. Count two physical units; never merge based on model alone.
4. **Duplicate media:** four images show the same target serial from different angles. Count one unit, four evidence artifacts.
5. **Placeholder enrichment:** exact property, linked placeholder, target plate and completed installation match. Propose update of the existing card, not create plus update.
6. **Cross-property conflict:** plate serial matches a card at another property. Hold relationship/creation; investigate scope or relocation rather than attaching across properties.
7. **Ignored filter:** purported property query returns rows from three properties. Treat as unscoped; authorized full pagination and local filtering required before absence/dedupe claims.
8. **Partial failure:** create returned an ID, detail readback matches, attach failed. Report one created record and partial failure; next attempt verifies state and repairs association, not another create.
9. **Dropped type:** write returns success but readback is generic category rather than approved exact type. Verification fails; no completed claim.
10. **Registration conflict:** registration and target plate disagree on serial. Plate controls unit identity; document the conflict and review date/warranty associations separately.
11. **Repair component:** replacement igniter on an existing furnace. Record furnace service evidence and repair note, not a newly installed furnace or standalone igniter asset.
12. **Age question:** attached visit is a tune-up. Do not use that visit as installation date; return confirmed date blank and supported manufacture inference separately.

## Validation expectations

A documentation validator checks frontmatter, resolving intra-package links, valid JSON examples and absence of restricted data. Synthetic cases specify expected decisions; merely reading them is not execution of an adapter, OCR engine or live service. Do not label these packages production-tested without separately running contract and integration tests against an authorized environment.

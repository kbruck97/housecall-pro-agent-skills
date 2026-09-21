# Source decisions and resolved conflicts

Base: the single inventoried hcp-trade-equipment-job-review source variant, read in full. Selected reusable references read: customer-existing-equipment-full-profile-workflow.md and customer-wide-profiled-equipment-json-schema.md. Historical case corpus and backup files are not included.

Retained: installed versus proposed versus serviced-existing separation; physical-unit versus existing-record modes; all-history review; per-property dedupe; real-unit brand/identity discipline; replacement-aware chronology; current live equipment overriding stale prompt inventories; strict JSON output; and exact write/readback/linkage verification.

Resolved contradictions explicitly:

- The source main file's late conservative exclusions override older references that independently tracked thermostats, coils, pressure tanks, or geothermal components. The portable default preserves that conservative boundary. Broader trade policy is a separately approved version, never inferred from older examples.
- Existing-record cardinality and physical-unit cardinality differ. The package accounts for every source record in a disposition ledger while outputting physical units separately. Excluded records do not become allowed equipment solely because they exist in the CRM.
- Sparse completed performed service can prove a real existing unit even without make/model/serial. This is allowed for profiles but does not bypass the stricter installed-new mutation gate.
- Source references disagree on earliest versus latest progress-invoice dates and whether repeated billing is service history. This draft uses actual work/commissioning evidence; an unproven exact date stays unknown, and accounting repeats do not become visits.
- Source transport notes disagree on CSRF and include fixed private endpoint/auth recipes. This draft requires a real opt-in adapter contract and does not publish either historical claim as universal behavior.
- Source nameplate rules conflict with older inferred-brand/capacity shortcuts. Identity must be directly supported; derived specifications require a verified technical source and an explicit derived basis.
- Bare plural unit wording is not an exact count. Hold uncertainty rather than inflate physical rows from a linguistic minimum.
- Candidate exclusion is an analytical disposition, not a delete/retire command. Probe-create/delete discovery is removed.

No private authentication scripts, profile paths, tenant names, customer/job IDs, credentials, phone destinations, media, or case filenames are redistributed. Optional dependencies are skill names in prose only. The inventory manifest/report guided source selection privately and are not bundled. The included RivetFlo-owned material has owner authorization for MIT release. Live adapter validation remains separate from offline editorial checks.

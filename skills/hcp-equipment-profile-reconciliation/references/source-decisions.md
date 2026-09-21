# Editorial source decisions

The source inventory reports one main/package variant for hcp-equipment-profile-reconciliation. Read its full main procedure and generic identity-and-canonical-type-adjudication reference; distill their rules rather than copying historical cases.

Retained: whole-property plans, one physical unit across linked representations, per-store address namespaces, installed-new versus serviced-existing semantics, parent/component distinctions, conservative identity/type decisions, writer-refusal handling, final current-state readback, and successful-call versus physical-unit counts.

Changed for portability: private equipment tool names are explicitly optional contracts; one-call-only transport and exact close JSON are conditional on a configured adapter. Add read-only default, explicit mutation approval, concurrency/idempotency checks, honest partial-store recovery, and bounded stop conditions. Separate accepted writes from verified business outcomes.

Excluded: historical customer case corpus, record identifiers, local deployment/configuration paths, private server bridge implementation, credentials, tenant-specific naming examples, and unverified current endpoint claims. The legacy umbrella's probe-create/delete advice is not adopted. Companion skills are named in prose, not linked outside this package.

This is editorial packaging, not a working adapter or a live validation result. The owner authorized this included material for MIT distribution; excluded source corpora and third-party material are not covered.

# Public distribution policy

This pack is released under MIT with explicit authorization from the owner of the included RivetFlo material. Historical source-license labels in NOTICE and the source-disposition ledger are provenance, not the current license of this distribution. Excluded sources, tenant records, vendor documentation and third-party trademarks are not relicensed.

## Payload boundary

The public payload comprises the root maintenance guide, README, LICENSE, NOTICE, document index, and text files under skills, docs, scripts, tests, examples and schemas. The packaging helper excludes the internal planning document. Version-control metadata, internal branch-start records, private discovery inventories, source resolvers, credentials, profile configurations and tenant case histories are never included. The generated PACKAGE_MANIFEST.json binds every selected file to its SHA-256 digest.

Build into a fresh operator-owned directory outside the source checkout, stage with scripts/package.py, and run the validator and offline tests on the stage. Review the complete selected payload, not just changed files. Automated patterns do not prove that arbitrary prose is free of private information. A package checksum must be conveyed through a trusted channel; it is not a signature or origin guarantee.

For initial public publication, initialize a new repository from the verified staged files. Do not push the development repository's history: excluded files can remain in its commits even when absent from the latest tree. Keep the internal development records intact and separate. Subsequent public changes must pass the same privacy, license, link, contract and package checks.

## Capability boundary

Publication is not installation, live integration or tenant validation. This is an independent skill pack and offline helper library, not an official SDK or a Housecall Pro-endorsed product. No credentials, HCP/provider calls, customer messages or production mutations are needed to build, validate or stage it. Runtime adapters, tenant entitlement, permissions and provider behavior need separate verification and scoped authorization.

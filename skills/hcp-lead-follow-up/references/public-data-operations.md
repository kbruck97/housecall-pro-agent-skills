# Public lead and pipeline operations

Evidence: official changelog https://docs.housecallpro.com/docs/housecall-public-api/06ba3d648e345-changelog in discovery snapshot 2026-09-21. This establishes operation families, not complete request schemas. Inspect the exact current endpoint body before any write. Local observations are not substitutes.

## Intake and lifecycle procedure

1. Bind company, source inquiry, party/contact and requested property. Search complete current leads/customer/job/estimate evidence using documented filters and row scope checks. A shared phone or name is not a safe merge key.
2. Public lead list/create/get and lead-to-job/estimate conversion are documented, as is lead line-item listing. Discover the exact configured adapter and supported schema; do not invent paths from the family names.
3. Draft a create plan only after duplicate checks. Preserve source attribution and unknowns; set all notification/side-effect choices explicitly according to the schema. Return dry-run by default.
4. Conversion is a separate write, not a status label. Re-read the lead, confirm selected destination, customer/property, line items and scheduling intent, and obtain exact conversion authority. Submit once. On timeout inspect the original lead and linked target before retry; do not create a second job to repair uncertain conversion.
5. Pipeline status listing and status changes for leads, jobs and estimates are documented. Read current configured status IDs for the correct object type; labels alone are not IDs. Before a move record old/new status, expected transition, reason, automation/notification effects and approval. Never assume moving to “won” converts an estimate, books an appointment or collects money.
6. Read back the lead, destination link and resulting pipeline status. Report source→target receipt with verified fields and unresolved side effects. Parent/child records can partially succeed; repair needs its own plan.

Positive: conversion produces one exact linked job after readback, with scheduling still pending. Negative: marking the lead converted from a successful HTTP response while the target job cannot be retrieved, then telling the customer they are booked.

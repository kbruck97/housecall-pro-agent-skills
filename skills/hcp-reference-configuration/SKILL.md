---
name: hcp-reference-configuration
description: Use when inspecting HCP company and reference settings. Map documented catalogs, configuration authority, and unresolved operations.
license: MIT
version: 1.2.0
---

# HCP reference and configuration

Start with foundations (dependency skill `hcp-foundations`) and the [ledger](references/capabilities.json). Reference reads can affect many downstream decisions; global configuration writes are never incidental cleanup.

## Supported families versus gaps

| Family | Evidence-backed coverage | Limit |
|---|---|---|
| Company | `GET /company`; multi-location header; franchise metadata PATCH in changelog | No arbitrary company/admin CRUD implied |
| Employees | `GET /employees` with page/page_size; active employees, roles, permissions and tags | Home marketing copy mentions creation, but current endpoint group lists only GET; no employee-create payload verified |
| Job types / lead sources | List/create/update documented in changelog | Exact paths and payloads not extracted; no delete inferred |
| Tags / service zones | Official indexed list pages, with service zones also in changelog | Search/index evidence only; schema details require verification |
| Schedule settings | `GET /company/schedule_availability`; update operation listed in sidebar | Writes change shared booking policy; payload unresolved here |
| Booking windows | `GET /company/schedule_availability/booking_windows` | Availability is not a reservation |
| Routes | `GET /routes`, date in YYYY-MM-DD, page/per_page | Read grouping of employees, appointments, events and estimates; no route optimization or create inferred |
| Events | `GET /events`, page/page_size; event detail listed | Scheduled calendar events, not audit history; event writes not established |
| Business units | Fields visible in objects | Management API unverified |
| Checklists | Navigation category present | Methods, payloads, permissions and completion operations unresolved |
| Service plans | No CRUD established | Job/event recurrence does not establish membership billing or entitlement |

## Operational procedure

1. Resolve company and selection scope; avoid contradictory `X-Company-Id` and `location_ids`. Retrieve only the reference families needed for the decision.
2. Collect active employees completely before reasoning about assignment. A missing inactive employee is not necessarily a deleted user. Permission fields describe employee capabilities, not the caller's API authorization.
3. Store resource IDs with current labels and source time; do not treat names as stable keys. Report duplicates, stale foreign keys, and missing mappings without automatically “repairing” them.
4. For booking analysis, read organization settings and use required service duration. Resolution is explicit positive `service_duration` in minutes, otherwise configured `service_id` duration, otherwise documented 30-minute fallback. Service selection still filters eligible pros. Do not use the fallback as a claim that the actual job fits. The booking endpoint returns UTC window timestamps; resolve display in the organization's timezone.
5. Read relevant jobs/appointments, estimates, routes, and calendar conflicts. Preserve recurrence/all-day semantics. The events list has no documented date filter in this extract: do not invent one; collect the authorized scope and apply local window logic. Routes request `per_page`, not `page_size`.
6. Null schedule/local fields and incomplete roster/conflict reads block a safe availability claim. Local job display fields `time_zone`, `scheduled_start_local`, and `scheduled_end_local` were documented August 20, 2026; preserve UTC and timezone rather than replacing timestamps with naive local values. Recheck immediately before any separately authorized booking.
7. For a configuration change, obtain exact before/after approval, confirm dependent integrations and blast radius, fetch the full operation schema, and save a rollback plan. Submit only requested fields and verify exact readback. A report request cannot authorize changing schedules or employee permissions.

## Unsupported handoff

For checklist completion, employee creation, business-unit administration, or service-plan CRUD, return `verification-required` and identify the owner/schema needed. Never derive POST/PATCH routes from category names. Where no supported adapter exists, provide a manual office task; do not claim it was completed.

**Positive:** Report the active roster and route assignment conflicts with full paging evidence, while leaving dispatch unchanged.

**Negative:** A permissions object includes `can_edit_settings`, so the agent invents an employee admin endpoint. Refuse: object fields do not establish endpoint support.

Completion requires exact scope, collection coverage, source timestamps, explicit schema gaps, and no implicit global configuration changes.

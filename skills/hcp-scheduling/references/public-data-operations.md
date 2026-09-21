# Public schedule, dispatch and change boundaries

Sources: https://docs.housecallpro.com/docs/housecall-public-api/898190c92fb8b-schedule-windows ; https://docs.housecallpro.com/docs/housecall-public-api/c80920efe7ef1-booking-windows ; https://docs.housecallpro.com/docs/housecall-public-api/8d0d12e41a38b-get-routes ; https://docs.housecallpro.com/docs/housecall-public-api/5f8b2b787f4ba-get-events ; https://docs.housecallpro.com/docs/housecall-public-api/06ba3d648e345-changelog . Discovery snapshot attribution: 2026-09-21; no live verification.

## Collect and qualify

Read schedule settings, booking windows, active employees, events, service zones and routes using actual endpoint schemas. Routes use request `per_page`, response `page_size`; paginate fully. Events are calendar entries, not an audit stream; all-day/recurrence boundaries can affect conflicts. A current route is not an optimizer or permission to assign a technician. Validate qualifications, service zone, duration, travel/availability policy and tenant-local timezone. No complete roster/calendar means no definitive free-slot claim.

`time_zone`, `scheduled_start_local`, `scheduled_end_local` are documented local display fields; UTC fields remain unchanged and local values may be null. For DST ambiguous/nonexistent local times, require an explicit offset/zone-resolved instant and operator/customer clarification. Never attach the server timezone to a naive customer time. Availability is not a reservation: recheck immediately before commit.

## Mutations and distinct receipts

- Job schedule update/delete and dispatch employees are documented in the Jobs sidebar; estimate-option schedule update is separate. Fetch exact schemas before execution. No arbitrary appointment CRUD is inferred from an Appointments navigation category.
- A **reschedule** plan records old and new interval, timezone, property, staff and notification effects. Verify availability, approved quote/disclosure and explicit customer choice, then submit once. Read back exact interval and assignment; tell the customer only verified changes.
- **Deleting a job schedule is not canceling the job.** A cancellation request requires tenant policy and supported job-cancellation capability or human handoff. Do not claim job canceled from a schedule DELETE receipt; retain requested versus executed state.
- **Dispatch** is a separate staffing change. Re-read active eligible employee IDs, conflict data and target job; obtain scoped assignment authorization. Verify exact assignment afterward. No unsupported route-create/optimize/GPS write endpoint is supplied.
- **Schedule-settings update** is company-wide administrative change with broader impact than one booking. Require separate admin approval, before-state and rollback plan; never change global windows merely to fit one caller.

Timeout after booking/update is ambiguous. Read source appointments and transaction ledger before any retry. A scheduler-local pending hold or escalation receipt is not an HCP booked appointment.

Positive: approved new appointment readback confirms interval and assigned technician; previous interval is absent. Negative: deleting a schedule and telling the customer the job and invoice were canceled.

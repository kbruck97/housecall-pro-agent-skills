# Parameterized tenant policy—not installed business facts

Tenant overlays may narrow authority, select verified business policy and adapt intake. They cannot grant tools, bypass consent or manufacture live truth. Keep real configuration outside published skills. No named source tenant, employee, schedule, incentive or callback number is a portable default.

## Overlay contract

```yaml
schema_version: 1
tenant_ref: tenant_example
policy_revision: approved_revision_example
business_identity_ref: approved_business_record
service_area_ref: approved_territory_record
timezone: null # required before local appointment labels
callback_contact_ref: null # same-turn verified; never a remembered legacy number
service_catalog_ref: null
excluded_work_ref: null
referral_partner_rules_ref: null
maintenance:
  intake_mode: office_review # equipment_confirmed | onsite_assessment | office_review
  quote_model: office_review # equipment_plus_dispatch | drive_tier_visit | office_review
  materials_policy_ref: null
  membership_policy_ref: null
scheduling:
  policy_ref: null
  confirmation_mode: human_review
communications:
  channel: sms
  maximum_questions: 1
  cadence_policy_ref: null
  consent_policy_ref: required
  voice_disclosure_policy_ref: required_if_voice
escalation:
  monitored_queue_ref: null
  on_call_policy_ref: null
  response_sla_ref: null
```

Missing mandatory configuration means no promise or write, not inherited settings from a neighboring tenant.

## Meaningful source variants retained

- **Equipment-priced HVAC maintenance:** verify which property and current equipment list; pass the confirmed list consistently through quote, duration, availability and booking. Compound equipment keys must use the adapter's canonical taxonomy to avoid generic substring matches. Full visit totals may combine equipment lines and a separate maintenance dispatch fee. Travel/diagnostic fees are a different product. Member pricing is not one-time pricing.
- **Drive-tiered water-treatment maintenance:** an approved onsite-assessment policy may deliberately omit equipment interrogation. Collect address, obtain a live all-in visit quote, preserve materials caveat and technician-assessed scope. Do not add a second travel fee or infer drinking-water safety from symptoms/raw values. Non-maintenance troubleshooting intake may still collect equipment type and recent service.
- **Electrical trade overlay:** tenant-specific low-voltage/commercial exclusions, referral partners and service radius need verified configuration. Out-of-area requests may need review instead of automatic rejection. Generator warranty intake may require make/model/serial. Scheduling categorization must not demote a concrete electrical hazard; historical labels describing line-related work as sales are not safety overrides.
- **Plumbing trade overlay:** scope can span water heaters, boilers, treatment, appliance work and camera inspection; this does not imply every tenant offers each service. SMS requires natural typed intake rather than voice spelling/readback scripts. No unsafe repair instructions or unsupported service-area/price claims.
- **Complaint neutrality:** acknowledge frustration without accepting an unverified causal allegation; do not conceal confirmed facts or use brand protection to deny documented harm. Escalation copy remains receipt-gated.
- **Schedule policy variants:** weekday-specific grids, emergency-only days, estimator restrictions and named-technician requests are configuration, not universal slots. A preferred employee is a request until an authoritative assignment exists.

## Dormant maintenance selection

Use verified active units and completed service/install events, current agreements, suppression, recent conversations and existing lifecycle schedules. Exclude merged/removed parties, do-not-service flags, recent duplicates and inappropriate member audiences. Unknown sentiment stays unknown. Age/EOL ranges and seasonality can inform internal prioritization but not fear-based copy. Historical calendar capacity is only a shortlist signal; confirm current capacity before any approved outreach. Group systems into one visit only if supported by current tenant policy.

Synthetic draft: “Hello from the service office. Would you like help arranging preventive maintenance?” Add equipment names only with provenance and do not imply membership.

## Migration decisions

Source families: three CSR hub main variants, three customer-service variants, five tenant main variants across four trades, and one scheduling main variant. Newer default cross-lane consent/receipt controls supersede older guaranteed-reply, callback-soon and pending-booking promises. The HVAC complaint-neutrality variant is retained with honest acknowledgment of verified facts. Tenant prices, names, regions, incentives, credentials, ports and deployment paths are excluded. Historical tenant sources carried proprietary notices. The owner authorized this distilled RivetFlo-owned material for MIT release; excluded source files and tenant data are not distributed or licensed here.

# Lookup protocol

## Bounded discovery ladder

1. Exact model and target field in authorized manufacturer search or supplied documents.
2. Exact family plus installation instructions, product data, or dimensions.
3. Manufacturer product index or sitemap, then canonical product page and linked literature.
4. Authoritative distributor/dealer copy of the manufacturer document if primary access fails; verify issuer, revision, and applicability rather than trusting dealer prose.
5. Explicit UNKNOWN with coverage gaps if decisive evidence remains unavailable.

Some content systems expose a product-index JSON document or text-only page representation. Treat these as conditional discovery mechanisms, not a universal endpoint contract. Parse the actual envelope, identify model metadata, and follow canonical literature references. A permission error is not absence of the product; do not evade access controls or repeat requests indefinitely. Offline mode omits all network steps and uses the same applicability test on available documents.

## Applicability matrix

For each candidate source, record the exact input model and document's literal model/family token; whether the mapping is exact, documented-family-member, or uncertain; region/market; revision; capacity suffix; cabinet variant; orientation; fuel suffix; and relevant accessory configuration. Mark irrelevant fields not-applicable with a reason rather than silently omitting a decisive dimension.

An input mismatch must not be silently repaired. Preserve both original and hypothesized correction and require a legible plate or reliable nomenclature before selecting the correction. Manufacturer parent-company or warranty-program branding does not automatically identify the consumer nameplate brand.

## Filter-size protocol

Determine whether the question concerns factory rack, field-added cabinet, or return grille. Consult the exact cabinet/orientation row, not just furnace input capacity. Check whether dimensions are nominal or actual, whether the table lists a minimum area rather than dimensions, number of filters, thickness, and configuration-dependent alternatives.

If a manual allows several return/filter arrangements, report those alternatives only when requested; they do not identify the installed arrangement. A furnace-only model cannot establish a field cabinet's filter. Ask for the final cabinet label or measured existing filter; do not infer from an old pre-modification photo. Do not convert a minimum face area into a rectangular size without a documented approved arrangement.

## Capacity and nomenclature protocol

Use the manufacturer's quantity label. Record heating versus cooling, input versus output, min/max versus nominal/rated, test conditions, and units. Separate combi-boiler heating and DHW circuits even when a product title presents one larger number. Do not call DHW input space-heating output.

If model nomenclature establishes nominal cooling capacity, cite that decoding rule and label the result nominal. A common numeric convention without family-specific confirmation is insufficient. Unit conversions must be calculated with a tool and record input, factor, rounding, and result; do not manufacture precision beyond the source.

Refrigerant may differ between adjacent generations with similar names. A newer family page is not evidence for the older installed family. Likewise, a furnace model does not identify refrigerant in a separate outdoor unit. Unknown is safer than a plausible but incompatible specification.

## Fuel and dates

A nameplate's fuel suffix is literal identity evidence. Documented conversion work can describe current configuration but does not rewrite the manufacturer's model string. Do not infer conversion from an orifice sale alone. Manufacture date from a supported serial-decoding source is not installation date; service date is neither. Generic literature never establishes the serial of a particular unit.

## Citation and privacy control

Retain a source receipt with document title, issuer, revision, page/table/row, short relevant fact, and applicability reason. Use safe document aliases in shared artifacts; restricted source retrieval details remain in the authorized evidence store. No customer filenames, identity/contact information, signed links, credentials, or equipment record identifiers belong in reusable examples. Public research queries should use model/fact terms, not customer identity or job text.

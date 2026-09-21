# Synthetic acceptance cases

All fixture names and equipment strings here are invented. These cases test decision behavior; they are not claimed image/OCR execution results.

| Case | Synthetic input | Expected outcome |
|---|---|---|
| A | Target outdoor unit; only indoor head plate matches recorded serial | Wrong component; strict not-found, no copied values |
| B | Same model on two cabinets; plate serials `SYNTHETIC-A-01` and `SYNTHETIC-A-02`; target binding unresolved | Hold target binding; cannot confirm by model |
| C | Target-bound plate has model `DEMO H-07 X`; record says `DEMO H-07X` | Corrected in exact mode; retain the space |
| D | Actual target plate make legible, model/serial glared | Partial transcription; unknown model/serial; no full confirmation |
| E | Registration agrees with record; target physical plate differs | Plate controls strict result; disclose document conflict separately |
| F | Only completed, unit-specific handwritten maintenance worksheet | Plate-only not-found; document-enabled service evidence with worksheet provenance |
| G | Generic product brochure shows multiple models | No installed-unit model or serial; no inferred asset from brochure art |
| H | Explicit carton-enabled task; carton uniquely bound to target | Carton identity permitted and labeled; installation still unproven |
| I | Same carton in default strict task | Excluded; no plate confirmation |
| J | Two adapter entries download identical bytes | One inspected artifact, one duplicate, not two witnesses |
| K | One original plus a technician avatar URL in page data | Only original counts as attachment evidence |
| L | EXIF-rotated image; initial crop misses actual label | Reorient and recrop before judging legibility |
| M | Human serial tail ambiguous; decoder has plausible value | Unknown in strict human-readable mode; do not promote decoder automatically |
| N | Heat-pump target; legible compressor label and unreadable unit plate | No copying compressor serial onto parent |
| O | Manufacturer plate has Model and Part Number but no serial | Model may be retained; serial unknown |
| P | Recorded make is consumer brand; plate prints different legal manufacturer | Exact mode corrects printed make; normalized mode follows explicit brand policy, not ad hoc exception |
| Q | All media inaccessible | Blocked internally, not an exhaustive no-nameplate result |
| R | Target unit is clearly visible, separate badge legible, data label blurred | Strict make/model/serial unknown unless an actual data-label field is readable |
| S | Plate dates manufacture; job is annual service | No installation date inference and no installed-new claim |
| T | Repeated enhancement produces plausible but inconsistent last character | Stop, unknown; request better image |

## Partial-result projection example

Internal field observations may retain a supported make while model and serial remain null. If the caller requires all three fields to verify and only accepts three verdicts, use the agreed `not_found` projection with the reason “target plate partly readable; required model and serial unresolved.” If the caller requires all fields blank on not-found, blank them in that projection while retaining the make observation privately. Do not claim the entire plate was absent.

## Review receipt example

For case J with both downloads inspected through one selected original, count two successful downloads, one unique artifact, one duplicate, and one unique inspected artifact. Target/field checks can pass only after actual visual inspection; deduplication alone proves no characters. Record schema/privacy checks independently. Remote writes remain zero, even when the comparison verdict is corrected.

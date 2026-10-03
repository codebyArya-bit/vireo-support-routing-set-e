# Validation: measured results and their limits

## Frozen model and sampling

`docs/model-freeze.json` records the SHA-256 of `src/core.py` before choosing the evaluation set. The first 100 explored records were excluded. Using seed 20261004, a uniform sample of 100 was selected from the remaining 11,541 reporting-window tickets. The assistant reviewed opening messages and notes with original tags, assigned teams and resolving teams hidden. It assigned root-issue reference labels before computing predictions. No classifier or threshold changed afterwards. Private label files retain the evidence and permit evaluation reproduction.

**Important:** the same ChatGPT/Codex assistant developed the model and reviewed labels. This is an assisted check, not independent human ground truth. No certified human accuracy or production claim is made. The sample shares message templates with the development pack; performance on new language can be worse.

## Results

| Measure | Opening message only | Opening + closing notes |
|---|---:|---:|
| Reviewed sample | 100 | 100 |
| Accepted classifications | 61 | 85 |
| Incorrect accepted classifications | 3 | 1 |
| Needs review | 39 | 15 |
| Acceptance coverage | 61% | 85% |
| Error among accepted | 3/61 = 4.92% | 1/85 = 1.18% |
| Wrong or needing review | 42/100 = 42% | 16/100 = 16% |
| 95% Wilson interval for accepted-error rate | 1.69%–13.49% | 0.21%–6.37% |

These intervals quantify sampling uncertainty under the assumed reference labels; they do not correct reviewer bias or template dependence. The retrospective column is not live-routing performance. Root-issue labels sometimes rely on closing notes, so intake ambiguity is exposed rather than filtered out.

## What gets it wrong

All three accepted intake errors were order/address changes mistaken for Delivery & Shipping. For example, “entered wrong pincode” and “ordered the wrong colour, don't ship it” can resemble delivery descriptions. The accepted retrospective error was an order/address-change case. Sparse euphemisms (“dies by lunchtime”) and unusual language commonly abstain. A snapped watch strap was reviewed as Hardware & Controls but abstained because the synthetic taxonomy has poor coverage for accessory faults.

The sample has just one Hardware & Controls ticket, two Audio Quality, three Account & Login and three App & Firmware. No strong class-level accuracy claim is possible. `output/validation.json` includes per-class counts and the confusion matrix, with anonymised case IDs. `evaluation_rows_PRIVATE.csv` links to exact private audit rows.

## Separate business-case check

The same assistant individually read all 77 selected Q2 transfer opportunities. No clear non-delivery case was found. Every selected record has an accepted opening-text Delivery label, initial Billing, a recorded Logistics resolving agent, completed status and at least one known transfer. This selected census supports the chosen case only; it does not estimate missed opportunities or population precision. Some closing notes are non-informative; human review remains necessary. The 50% prevention rate is a proposal, not a measured treatment effect.

## Data reconciliation and software checks

- 11,780 raw tickets = 11,641 reporting-window tickets + 139 earlier records.
- All five category/team counting bases reconcile to 11,641 tickets.
- 3,913 unknown transfers remain unknown; missing surveys are excluded from CSAT averages.
- 3,720 legacy completed timestamps are converted from UTC to IST; invalid chronology is excluded from duration metrics. 2,335 legacy resolutions preceded creation before the correction; none do after it in the scoped pack.
- No duplicated ticket IDs or exact event fingerprint groups were found. Fuzzy re-import deduplication is not implemented.
- Input file hashes are recorded for reproducibility. Duplicate attachment copies match byte-for-byte and are not ingested twice.
- Eight unit/integration tests cover date correction, missing values, dated/overlapping roster joins, classifier abstention, billing/delivery distinction, one-transfer savings arithmetic, report reconciliation, period exclusions and duplicate IDs.
- Clean Python execution uses only the standard library. Local HTTP endpoint checks and JavaScript syntax checks are documented in `docs/qa.md`.
- Rendered browser QA and automated screen recording could not complete: Chromium downloads were truncated. Do not interpret syntax/HTTP checks as rendered interaction proof.

## Before live automation

Have a Vireo lead adjudicate this sample and a fresh sample. Add labelled examples for order changes and accessory faults using a development split, then freeze and test a new holdout. Run a supervised four-week pilot; audit 30 routed cases/week, record actual avoided transfers, compare queue waiting and first-response breaches, and do not rank Tier 2 by volume.

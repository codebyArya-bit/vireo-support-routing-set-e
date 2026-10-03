# Run cost and monthly operating scenario

## Paid software / inference

The executable does not call any hosted model or API. It trains a 55-example TF-IDF similarity model in-process using Python's standard library; model weights are recreated locally. No API keys, downloads or pip installation are needed to run.

- One full supplied-pack analysis: 11,780 raw records, 11,641 in scope. Runtime paid-call count = **0**; API charge = **Rs 0**. Initial observed analysis time was 9.377 seconds on the build machine; this is not a latency guarantee.
- Vireo planning volume = 650/week × 52 weeks / 12 months = **2,816.67 tickets/month**.
- API cost/month = 2,816.67 tickets × Rs 0/ticket = **Rs 0**.
- If a run means a weekly 650-ticket batch, 650 × Rs 0 = **Rs 0/run**; 52/12 runs/month × Rs 0 = **Rs 0/month**.

ChatGPT/Codex assisted development and text review through the candidate's existing chat environment. There was no separately metered model API. Subscription price attributable to this build, electricity, machine cost and eventual hosting cost are unknown and are not falsely claimed to be zero.

## Human review is not free

Full-pack opening-text `Needs review` count is 4,403 / 11,641 = **37.82%**. Assuming one additional minute of review per uncertain ticket and policy agent cost Rs 165/hour:

2,816.67 × (4,403/11,641) = **1,065.35 reviews/month**.

1,065.35 × (1/60 hour) × Rs 165 = **Rs 2,929.72/month** of illustrative additional review effort. The corresponding full-pack review cost is 4,403 × Rs 2.75 = **Rs 12,108.25**. Actual review time is not measured. Existing support work may already include this review, so it is not necessarily incremental spending.

Gross quarterly routing target = **Rs 41,972.98** at 650/week. If every low-similarity ticket needs an extra minute, illustrative quarterly review cost is 8,450 × (4,403/11,641) × Rs 2.75 = **Rs 8,789.17**, leaving **Rs 33,183.81** before compute, implementation and training costs. This is a sensitivity scenario, not a forecast.

## Avoided-transfer arithmetic

Observed Q2: 77 qualifying detours / 2,364 tickets = 3.2572%. At 50% prevention, the eligible rate falls to 1.6286%.

- Observed Q2 gross target: 77 × 0.5 × Rs 305 = **Rs 11,742.50**.
- At stated Vireo volume: 650 × 13 × (77/2,364) × 0.5 × Rs 305 = **Rs 41,972.98**.
- At 25% / 50% / 75% prevention: **Rs 20,986.49 / Rs 41,972.98 / Rs 62,959.47** per quarter at stated volume.

Only one hand-off/ticket is counted. Refunds, replacement cost, SLA credits, repeats and Rs 9 lakh/year of hires are not added. Resolution delays may be courier/customer waiting; they are not treated as saved agent hours.

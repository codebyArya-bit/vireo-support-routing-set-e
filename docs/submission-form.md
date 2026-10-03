# Task 1 V2 — Submission answers (candidate completion required)

Candidate: Aryabrat Mishra. The original pack did not contain submission-form.md; this reconstructs the visible questions. The analytical answers below are drafted from the runnable tool. Actual hours are recorded as 1, confirmed by the candidate. The final public links and actual screen recording must be supplied before submission. This file is not presented as a completed form.

## What did you build, and what business outcome does it move? State the number and the money.

I built an offline Python support-routing decision tool with text categorisation, a review bucket, monthly category/team charts, and separate first-assigned versus recorded-resolving-team views. The business goal is to halve eligible Billing-to-Logistics detours from 3.26% to 1.63% of tickets. Q2 has 77 eligible cases out of 2,364 tickets. Preventing one hand-off in half gives 77 × 0.5 × Rs 305 = Rs 11,742.50 gross/quarter at observed volume. At 650 tickets/week: 650 × 13 × (77/2,364) × 0.5 × Rs 305 = Rs 41,972.98 gross/quarter. This is a proposed pilot target, not realised savings. An illustrative extra-minute review scenario lowers the latter to Rs 33,183.81 before implementation/compute costs.

## What does one run cost, and what would a month cost at roughly 650 tickets/week? Show arithmetic.

No paid inference calls. A full-pack run or a weekly batch has Rs 0 API cost. Monthly volume is 650 × 52/12 = 2,816.67 tickets; 2,816.67 × Rs 0 = Rs 0 API cost/month. The initial full-pack analysis took 9.377 seconds on the build machine. That is not a hardware-independent guarantee. Review effort is separate: opening-text uncertainty was 4,403/11,641 = 37.82%; at one extra minute each, 2,816.67 × 37.8232% × (1/60) × Rs 165 = Rs 2,929.72/month. Actual review time, electricity, hosting and attributable ChatGPT subscription cost are unmeasured.

## How do you know it works? Sample size, how checked, error rate and wrong cases.

I froze the model before a seeded random sample of 100 previously unviewed tickets, hiding exported tags/teams. ChatGPT/Codex assisted reference-label review from opening messages and closing notes before predictions were calculated. Opening-only: 61 accepted, 3 wrong, 39 review; error among accepted 4.92% (95% Wilson interval 1.69%–13.49%). With closing notes: 85 accepted, 1 wrong, 15 review; 1.18% accepted error. That second number is retrospective, not live-routing accuracy. The same assistant authored and reviewed the model, so independent human validation is still required. Address/order changes were mistaken for delivery; unusual wording and accessory faults often abstain. The same assistant separately read all 77 business-case candidates, finding no clear non-delivery case. Eight automated tests check policy/data invariants and reconciliation.

## Did you change, narrow or push back on the client's ask? What, when and why?

Yes. After reading the email thread and doing the first data inspection, I retained the monthly charts but pushed back on giving two hires to the biggest initial queue. Billing's queue mixes payment and delivery issues: 696 of its 2,425 in-window tickets are recorded against Logistics agents. Logistics has 2,574 recorded-agent tickets versus Billing 1,798 and median elapsed resolution of 26.03h versus 1.22h. These are process/capacity warning signs, not handling-hour proof. I recommend a supervised routing pilot before allocating Rs 9 lakh/year of hires, then a separate capacity review including shift coverage and courier delays. I did not automatically award the hires to another team.

## What is wrong with what you are handing us? Be specific.

The intake classifier leaves 39/100 evaluation cases needing review and wrongly accepts 3. Its similarity scores are not calibrated probabilities. The same AI assistant labels and checks; no independent Vireo adjudication. There is little evidence for rare Hardware & Controls cases and novel message styles. The model can confuse address changes with delivery. Closing-note analysis uses future information and is only retrospective. Exact fingerprints do not catch all fuzzy legacy re-imports. The recorded-agent team is not a full transfer path; elapsed resolution includes waiting. Old refund units are unresolved. The 50% prevention rate and one-minute review time are assumptions. The server is local-only and not production hardened. Browser-rendered interaction QA and actual screen recording remain unfinished because Chromium downloads were truncated. Final public links and the actual recording must be supplied before I submit.

## What did you deliberately leave out, and why that rather than something else?

I left out live helpdesk integration, automatic routing, cloud/LLM APIs, shift-level hiring optimisation, exhaustive fuzzy deduplication, same-issue FCR measurement and refund/replacement fraud attribution. They require labels, workflow history or handling-hour data not safely inferred here. I prioritised a tool that starts without credentials, reconciles the charts, separates intake from retrospective evidence, and quantifies one conservative process intervention. The unknown category stays visible instead of making the chart look complete through forced labels.

## Anything you built or found that nobody asked for?

I added initial-versus-recorded-agent attribution, an explicit review category, opening/closing disagreement flags, timestamp and missing-value diagnostics, a 25%/50%/75% savings sensitivity, and costed human-review assumptions. I found 139 records outside the stated period, legacy UTC resolution timestamps and 3,913 unknown transfer counts. I also found a mismatch between the brief's 650/week planning volume and the much smaller export, so I show both observed-volume and scaled-scenario savings.

## What did you use AI for? Tools/models, help, waste, discarded work. Link recording.

I used ChatGPT/Codex for pack interpretation, record inspection, coding, synthetic taxonomy examples, reference-label review and drafts. The executable uses a local TF-IDF nearest-example classifier, not an LLM API; no paid model calls. I do not invent an exact underlying chat model version. AI sped up implementation, but same-assistant evaluation creates correlated-error risk. I rejected noisy exported tags as training truth, resolver team as gold labels, automatic volume-based hires, hindsight accuracy claims, forced uncertain labels and an unnecessary paid API/cloud stack. Automated browser installation for recording failed; I prepared an actual-tool recording walkthrough instead of substituting slides.

Recording URL: PENDING — record the working tool using docs/recording-script.md and insert a verified publicly readable link. Do not submit this draft field.

## Your Public Google Drive Link

PENDING — verified upload/share link required; upload public-code bundle and memo/recording, not raw customer data. Access must be Viewer / Anyone with the link. Do not submit a private link.

## Someone picks this up Monday and you are unreachable. The three things they need to know.

1. Use Python 3.11+, follow README.md, open the precomputed dashboard with python serve.py, or regenerate with the five private CSVs. No packages/API keys are required. Do not publish _PRIVATE outputs or customer data.
2. Use opening-only classification for intake; closing notes are retrospective. Review abstentions and conflicting labels. Missing transfers stay unknown, legacy resolution timestamps get +05:30, and Tier 2 is not ranked against Tier 1 on volume.
3. The financial target assumes one avoided hand-off in 50% of 77 Q2 cases. Validate labels with Vireo staff, pilot for four weeks, audit 30 routed cases weekly, and have Finance reconcile actual savings before deciding headcount.

## Honest hours spent. One number.

1

## Github Repo Link (Public)

https://github.com/codebyArya-bit/vireo-support-routing-set-e

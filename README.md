# Vireo Audio — Support Routing Decision Tool (Set E)

An offline, AI-assisted support analysis tool by Aryabrat Mishra. It questions the proposed two hires in Billing by separating the queue a ticket first entered from its issue and recorded resolving team.

**Business target:** halve the eligible Billing-to-Logistics detour rate from **3.26% to 1.63% of all tickets**, worth approximately **Rs 41,973 per quarter at 650 tickets/week** in gross avoided hand-off costs. At the actual export's Q2 volume, the same target is **Rs 11,743**, not Rs 41,973. This is a proposed pilot target, not realised savings.

## Start on a clean machine

Needs **Python 3.11 or later** and a modern browser. No pip packages, API keys, database, network calls or model downloads.

1. Download/extract this repository and open a terminal in its directory.
2. Run the tests:
   ```sh
   python -m unittest discover -s tests -v
   ```
3. Open the included aggregate Vireo dashboard:
   ```sh
   python serve.py
   ```
   Visit **http://127.0.0.1:8765**. Try the opening-message classifier and switch between category and team charts or filter categories within an initial/recorded team. Ctrl+C stops the server. The precomputed dashboard also opens directly as `output/dashboard.html`; only the interactive classifier requires the server.
4. Reproduce the pipeline without private data using the clearly labelled synthetic pack:
   ```sh
   python run.py --data demo-data --out demo-output
   python serve.py --out demo-output --port 8766
   ```
   Visit http://127.0.0.1:8766. The banner identifies synthetic data; its numbers are not Vireo findings.
5. To reproduce the Vireo results, place the supplied five CSVs in `private-data/` using canonical filenames `tickets.csv`, `agents.csv`, `products.csv`, `orders.csv`, `customers.csv`, then:
   ```sh
   python run.py --data private-data --out private-output
   python serve.py --out private-output
   ```
   Original UUID-prefixed filenames are also supported. Do not mix different pack versions. The supplied `(1)` files are byte-identical copies; ingest one set. The PDF policy and email thread informed definitions; the runtime does not parse them.

On Windows, use `py` instead of `python` if needed. Bind remains loopback-only; do not expose this un-authenticated prototype on a public server.

## What is in this tool

- `src/core.py`: small supervised TF-IDF nearest-example text classifier, 55 authored synthetic examples, word/bigram/character features. It is statistical text classification, not an LLM. ChatGPT/Codex assisted development and reference-label review.
- `run.py` / `src/analysis.py`: date/window handling, dated agent assignment joins, diagnostics, monthly category/team breakdowns and transfer-cost business case.
- `src/dashboard.py`: standalone aggregate charts, filter controls, accessible tables, CSV download and local classifier demo.
- `evaluate.py`: frozen-model evaluation using the private review file; `output/validation.json` contains aggregate evidence.
- `output/`: Vireo aggregate dashboard, summary, monthly breakdown, team metrics and validation results.
- `docs/`: memo, submission draft, decisions, prompt/version log, costs, validation and recording walkthrough.

## Classification and uncertainty

Opening-message predictions are the routing view. Opening + closing-note predictions are retrospective and cannot be used as intake accuracy. When the two accepted labels conflict, the retrospective category is `Needs review`. Score <0.27 or top-two margin <0.035 also abstains. Scores are cosine similarity, not confidence probabilities.

On a frozen-model random 100-ticket assistant-reviewed check:

| Mode | Accepted | Wrong accepted | Needs review | Accepted error |
|---|---:|---:|---:|---:|
| Opening text | 61 | 3 | 39 | 4.92% |
| Opening + closing text | 85 | 1 | 15 | 1.18% |

Same AI assistant authored and reviewed; no independent human accuracy claim. First mode leaves 42/100 wrong or needing review. Closing-note mode leaves 16/100 wrong or needing review. See `docs/validation.md` for intervals, failures and sampling limits. No thresholds were changed after this sample.

## Data and decision rules

- Scope: tickets created 1 Jan 2025 through 30 Jun 2026 IST. 139 raw rows are earlier; excluded, not silently treated as 2025.
- Legacy resolution timestamps: +05:30 per policy §9, applied only to `legacy_fd`; creation/first response are already IST. Invalid chronology remains flagged/excluded from durations.
- Agent attribution: `agent_id`, assignment effective at resolution for completed tickets; creation for open/pending. Unknown/overlapping roster assignment → `Unknown`. It does not reconstruct intermediate teams.
- A raw duplicate ticket ID prefers current-helpdesk import. Exact event fingerprints across IDs are flagged, not automatically dropped. None of either appeared in this pack. Fuzzy re-import deduplication is not implemented.
- Missing legacy `transfers` is unknown, never zero. Blank CSAT is absent, never zero.
- Monthly charts use ticket creation month, including recorded-agent-team attribution; they are not a resolution-month productivity ranking.
- Resolution elapsed time includes waiting; do not turn it into agent capacity or compare Tier 2 with Tier 1.
- No blanket refund-unit conversion: old monetary units are undocumented. No refund/replacement/credit amounts are added to routing savings.
- Direct order joins are checked against customer/SKU; no ambiguous customer+SKU fallback is invented. It is not needed for the routing case.

## Business arithmetic and cost

Q2: 77 eligible detours / 2,364 total tickets = 3.2572%. Each candidate has initial Billing, an accepted opening-text Delivery category, completed status, Logistics recorded resolving team and at least one known transfer. The same assistant separately read all 77: no clear non-delivery case found; this is not independent validation or a recall estimate.

Avoid one hand-off on half: 77 × 50% × Rs 305 = Rs 11,742.50 at observed Q2 volume. Scale only as a scenario: 650 × 13 × (77/2,364) × 50% × Rs 305 = Rs 41,972.98 gross/quarter. A two-hire expense of Rs 9 lakh/year is not claimed as saved.

Runtime paid API cost: **Rs 0**. Monthly volume: 650 × 52/12 = 2,816.67. API arithmetic: 2,816.67 × Rs 0 = Rs 0/month. Human reviews, compute/electricity and any ChatGPT subscription are separate; see `docs/costs.md`.

## Privacy and handoff

The public repository intentionally excludes original customer/order/ticket files, row-level predictions, private labels and contact details. Public artifacts contain aggregates and synthetic examples only. `_PRIVATE` files produced by your own run remain local. Do not publish them just because `.gitignore` exists.

Use a supervised four-week pilot, measure actually avoided transfers, review 30 routed cases/week and check delivery-queue wait times. Stop expansion if misroutes increase. A Vireo subject-matter reviewer must adjudicate the validation sample before live automation.

The task pack did not include `submission-form.md`; a reconstruction of the visible form is in `docs/submission-form.md`. It is explicitly not submission-ready until verified public GitHub/Drive/recording URLs are supplied. The candidate confirmed 1 actual hour; this is within the assignment’s five-hour cap.

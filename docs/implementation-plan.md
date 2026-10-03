# Vireo Support Implementation Plan

**Goal:** Produce a runnable, auditable routing decision tool and honest submission pack.
**Architecture:** Standard-library data pipeline, text classifier, aggregate HTML dashboard and local prediction endpoint. Offline execution is default.
**Tech stack:** Python 3.11+, unittest; plain HTML/JavaScript/SVG.
**Spec:** docs/design.md (user-approved scope).

## Global constraints
- No paid calls or network dependency to run.
- No raw customer data in public repository.
- Correct legacy UTC resolution only; preserve unknown transfers.
- Distinguish retrospective classification from intake classification.
- Monetary outcomes must state assumptions and observed denominators.

## Review focus
- Duplicate import identifiers and cross-system near duplicates: flag without unjustified deletion.
- Missing dates or invalid chronology: exclude invalid duration and expose counts.
- Multiple dated roster assignments: join at resolution, not by name.
- Ambiguous payment/delivery text: abstain when scores/margins are low.
- Small or unseen categories: disclose validation coverage and avoid accuracy guarantees.

## Tasks
1. Write unittest fixtures for chronology, window, roster boundaries, model abstention and business arithmetic; confirm failure, implement ingestion/classifier, rerun tests.
2. Build analysis command producing aggregates, row-level audit exports and interactive dashboard. Verify reconciliation and reproducibility on supplied pack.
3. Freeze classifier, independently assistant-label a seeded random sample after freezing, report total error/coverage/confusion and representative failures. Explicitly distinguish assistant review from independent human validation.
4. Generate one-page memo, cost arithmetic, prompt/version/discard log, submission form and recording script. Verify memo page count and render.
5. Test from isolated directory without installed packages. Package public source separately from private data. Save final bundles. Publish only through available authorised account capabilities.

Execution: native in this session; independent agent delegation is outside the approved scope.

# Vireo Support Decision Tool
Approved scope: an offline Python tool, retrospective category analysis, independent review flags, requested monthly category/team charts, recent-quarter routing business case, validation, Priya memo and submission answers.

Python 3.11+, standard library only. Classifier is a small supervised TF-IDF nearest-example model trained on authored synthetic examples; no network or paid API. Its similarity scores are not probabilities. Optional local Ollama inference is an explicit separate mode, never necessary to run. Customer-message-only predictions support routing; closing notes can support retrospective analysis but cannot justify a live-routing claim alone.

Jan 2025-Jun 2026 is the reporting window. Preserve out-of-window data in diagnostics. Correct only legacy resolution timestamps by +05:30; transfers missing means unknown. Roster joins use agent_id and dates, and unmatched/ambiguous assignments remain unknown. Resolver attribution for unresolved tickets is labelled recorded-agent team, not work completed. No category tags or agent teams enter the model features. Forecast savings assume one avoided transfer, not all hand-offs, and are proposed, not realised.

Public package contains code, synthetic examples and aggregate report only. Raw customer/order data and row-level outputs remain in the private working bundle. README instructions work without credentials. The actual screen recording, honest human hours and account-hosted submission URLs cannot be invented.

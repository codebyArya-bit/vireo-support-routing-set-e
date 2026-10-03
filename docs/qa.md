# Verification evidence

Environment: Python 3.12 on Linux, tool requirement Python 3.11+. Pure Python standard library at runtime; Node used only for development-time JavaScript checks. Browser plugin not available. Playwright module was present but no Chromium executable; the attempted browser download repeatedly returned truncated files. Rendered desktop/mobile and screen recording checks remain pending.

| Check | Result |
|---|---|
| Eight unit/integration tests | Passed |
| Frozen model hash / independent-of-tags input | Passed; same-assistant labels are disclosed |
| 11,780 raw = 11,641 in scope + 139 earlier | Passed |
| Monthly totals reconcile for all five counting bases | Passed |
| Category-within-team cross aggregation | Passed |
| JavaScript syntax | Passed after fixing escaped newlines in emitted HTML |
| DOM-control logic in Node harness | Passed: initial data, Q2 filter, Billing filter, team basis, reversed empty range |
| Local dashboard HTTP | 200; meaningful HTML |
| Local prediction endpoint | Passed: delivery, missing-order payment, refund and nonsense abstention |
| Malformed JSON | 400, server remains alive |
| Clean-machine smoke test | Python -S, no site packages; demo pipeline and all tests pass |
| One-page memo | One A4 page; rendered PNG inspected for clipping and readability |
| Actual rendered browser interaction | Not completed; browser download failure |
| Actual screen recording | Not completed; walkthrough script supplied |
| Public GitHub repository | Not created; connector has no repository creation operation |
| Anyone-with-link Drive permission | Not set; connector shares only with a person/domain |

The Node harness exercises JavaScript logic with a minimal document stub. It does not prove rendering, layout, real browser download behavior or accessibility. The actual browser check is left explicit rather than inferred from syntax/HTTP success.

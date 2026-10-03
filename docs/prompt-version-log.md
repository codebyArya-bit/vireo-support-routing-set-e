# AI use, prompts, versions and discarded work

This is an honest log of this chat-assisted build, not a fabricated multi-model conversation.

## Actual input prompts

- Candidate supplied the Task 1 V2 / Vireo Audio Set E brief, all eight attachment types and the visible submission questions. Key verbatim excerpt: “Whichever team has the most volume gets the next two hires.” The task explicitly allowed AI tools and required disclosure.
- Candidate approved the proposed scope with the exact message: “I agree to this”.

The assistant's proposed scope was a small Python tool with text categories, uncertain-case review, monthly initial-versus-resolving-team charts, a transfer-cost routing target, validation, a memo, answers and a recording script. This was an in-chat design, not a separate model API prompt.

## Actions taken with AI

ChatGPT/Codex read the README, policy and thread; inspected records; wrote Python/HTML; authored 55 synthetic classification examples; read a 100-ticket blinded text sample and assigned labels before calculating predictions; separately inspected the 77 selected business-case records; drafted the memo and answers. No paid inference API, local LLM or external model service was called by the runnable tool. The exact session model identifier is not exposed in the deliverable and is not invented.

## Versions actually changed

**Exploration:** raw exports and initial queues. 11,780 raw records, including 139 outside the stated period. A direct roster join showed Billing assigned tickets often end in Logistics. This alone was not accepted as gold classification.

**Working tool:** period limited to 11,641 rows, legacy resolution timestamps corrected, recorded agent attribution joined by dated ID, cosine text model added with an explicit review threshold. Added opening-only versus opening-plus-closing views and conflict flags. Q2 eligible transfer arithmetic replaced a volume-only hiring verdict.

**Frozen evaluation / handoff:** froze `src/core.py` hash before selecting the evaluation sample, reviewed 100 new tickets, then measured predictions. Added separate intake and retrospective validation, costs and uncertainty disclosures. The classifier/thresholds were not tuned after seeing this holdout. This is a review/handoff revision, not a claimed model improvement.

## What was thrown away or rejected

- Rejected initial category tags as training labels: this would repeat the intake bot's errors.
- Rejected a direct “team with most tickets wins hires” answer: counts do not show effort, shift coverage or waiting cause.
- Rejected treating the resolving team as truth: an invoice case was resolved by Logistics.
- Rejected using closing notes to advertise live-routing accuracy.
- Rejected claiming every transfer on an eligible ticket disappears; financial case uses one.
- Did not implement an LLM API/cloud UI, because API cost, secrets and installation fragility were unnecessary for this scope.
- Did not force low-similarity cases into Other or tune after the holdout to improve the score.
- Browser installation for automated recording/rendered QA failed: Chromium downloads arrived truncated. No synthetic slide video is substituted for a real screen recording.

## Cost and limitations

No paid API calls: Rs 0 measured runtime API cost. Candidate's ChatGPT subscription, human time, machine power and eventual hosting cost are separate and unknown. AI saved implementation and inspection time, but correlated model/reviewer errors remain a major limitation. The assisted check is not independent human ground truth. Optional real subject-matter review is the next validation step.

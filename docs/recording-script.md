# Three-minute screen recording walkthrough (no slides)

Status: script and local tool prepared; an actual candidate screen recording is still required. Automated Chromium installation failed in the build environment, so no video was manufactured.

Record your screen and voice using Windows Snipping Tool video, OBS, or a phone. Maximum 3:00; aim for 2:30. Keep customer data and personal account details off-screen. Use the public aggregate dashboard and synthetic text only.

**0:00-0:25 — Actual prompts.** Open `docs/prompt-version-log.md` in an editor. Say: “I used ChatGPT/Codex with the Vireo brief and supplied pack. I approved an offline tool that keeps the requested charts but questions the volume-only hiring rule. I did not use a paid inference API.” Show the two actual prompt entries, not invented prompt conversations.

**0:25-0:50 — What changed.** Scroll to versions. “The raw export had 11,780 rows. I excluded 139 outside the reporting period, corrected legacy resolution times to IST, and separated first routing from recorded resolving teams. I then added text classification with a review bucket and froze the model before evaluation.”

**0:50-1:25 — Live working tool.** Run `python serve.py`; open http://127.0.0.1:8765. Change Counting basis from Opening text to First assigned team, then Recorded agent team. Filter April–June 2026. Show that the charts and downloadable table update. Try “Payment successful but order not delivered” and “Money debited but order not showing” using the classifier button.

**1:25-1:55 — Business number.** Scroll to the business goal. “There are 77 eligible Q2 detours out of 2,364 tickets. Halving that rate saves around Rs 11,743 at observed volume. At the brief's 650 a week, it is around Rs 41,973 gross per quarter. That assumes half can be prevented and counts one avoided transfer; it isn't money already saved.”

**1:55-2:20 — Evaluation and limits.** Open `docs/validation.md`. “A frozen-model, 100-ticket assistant-labelled check had 61 accepted intake classifications, three wrong, and 39 needing review. With closing notes it accepted 85, one wrong; that is retrospective only. I have not claimed independent human accuracy.”

**2:20-2:40 — What was discarded.** Return to the log: “I rejected training on noisy tags, automatic headcount allocation, treating resolver team as ground truth, and forced labels for ambiguous tickets. I omitted live helpdesk integration to keep it reproducible within scope.” Stop before 3:00.

Upload the real recording to the submission Drive folder; set Viewer access to Anyone with the link and test it in a signed-out browser. Paste the verified link into `docs/submission-form.md`.

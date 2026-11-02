# Writing and running UPSC-style practice

## The formats UPSC actually uses (mix them)

1. **Statement-correctness**
   "Consider the following statements: 1. … 2. … 3. … Which of the statements given above is/are correct?"
   Options: `1 only / 2 only / Both 1 and 2 / Neither 1 nor 2` (two statements) or `1 and 2 only / 2 and 3 only / 1 and 3 only / 1, 2 and 3` (three).
2. **"How many of the above"** (dominant since 2023)
   "How many of the above statements are correct?" → `Only one / Only two / All three / None` (or Only one…four). Harder because elimination between options no longer works; each statement must be judged.
3. **Match the pairs**
   "Consider the following pairs: Term — Description … How many of the above pairs are correctly matched?"
4. **Assertion–Reason** (rare recently, still appears): "Statement I … Statement II … Which one of the following is correct in respect of the above statements?" with options about whether II explains I.
5. **Direct / single-fact**: "Which one of the following…" — usually conceptual (e.g. which DPSP is Gandhian).
6. **Passage/context-hook**: "With reference to X, consider the following…" where X is a term from the news but the statements test static facts.

## Rules for every question you write

- One source of truth per statement: a fact from the Constitution text, NCERT, or the standard book. Don't test things that textbooks disagree on.
- Exactly 4 options, exactly one defensible answer. If you can argue two, rewrite.
- Build the trap deliberately: change ONE word in a true statement (a number, a House, "may" → "shall", "President" → "Governor", "statutory" → "constitutional"), or swap two paired items.
- Static only unless the learner asked for current affairs; never test facts that may have changed since your knowledge cutoff without flagging it.
- Explanation: 2–4 sentences, one line per statement stating the deciding fact. Finish with the trap in one phrase ("Trap: Rajya Sabha has 14 days, not 1 month").

## Running a practice session

1. Ask (or infer from the plan) the subject and topic range; default to the chapter the learner studied most recently.
2. Give 5–10 questions **without answers first**, numbered, options a–d. Ask the learner to reply with answers like `1b 2a 3d …` and which ones were guesses.
3. Score with UPSC marking: +2 correct, −0.667 wrong, 0 skipped. Report: score, accuracy on attempted, and guess-accuracy separately (good guessers should attempt more; bad guessers should skip more).
4. Explain every question, wrong or right. For wrong ones, name the type of error: *fact not known*, *fact known but misread*, *trap word missed*, *over-attempted*.
5. End with the 2–3 facts to re-read and whether the verdict is **exam-ready (≥70%)**, **revise notes (50–69%)**, or **re-read the source (<50%)**.

For a ready-made verified bank (99 questions across all subjects), read `mcq-bank.json` and draw from it before writing new ones; it is JSON with `subjects[].mcqs[] = {topic, q, options[4], answer (0-based), explanation}`.

## Teaching elimination (do this explicitly in mock analysis)

- Absolute words — "only", "all", "every", "always", "never", "cannot", "directly enforceable", "mandatory" — flag the statement for suspicion; most UPSC traps are a true fact with one absolute inserted.
- Over-specific numbers that the learner has never seen are more often wrong than right.
- In "how many" questions, if one statement is certainly wrong and one certainly right, the answer is bounded; attempt only if the remaining statement can be reasoned.
- In match-the-pair, one confident wrong pair usually decides the answer.
- Rule for attempting: attempt if you can eliminate to two options and have a lean; skip if it's a pure coin toss on three or more.

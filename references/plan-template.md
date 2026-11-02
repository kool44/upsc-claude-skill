# Plan templates

Use `scripts/make_plan.py` for the calendar maths; use this file for the shape of a week and a night, and the trimmed source list.

## Phases (why three phases)

| Phase | Share of time | Purpose |
|---|---|---|
| Foundation (first reading) | ~55% | One source per subject, chapter by chapter, PYQs after each chapter, short notes |
| Revision | ~20% | Second pass from notes, PYQs by subject in one sitting, sectional tests |
| Mocks | ~25% | Full-length tests at 9:30 AM, analysis, 3rd/4th revision, current-affairs compilation |

Shrink the foundation phase when time is short; never the mock phase. Prelims is an elimination exam, and elimination is a skill learned in mocks.

## Source list, trimmed for a working professional

| Subject | Use | Don't use (before Prelims) |
|---|---|---|
| Polity | Laxmikanth, whole book | Bare Acts, D.D. Basu |
| Modern History | Spectrum (skip long appendices) | Bipan Chandra for Prelims |
| Art & Culture | Singhania selected chapters + PYQs | Whole Singhania |
| Ancient/Medieval | PYQ-driven from old NCERTs | Full old NCERT reading |
| Geography | NCERT XI Physical + India Physical + atlas; XII selectively | G.C. Leong cover-to-cover |
| Economy | NCERT XII Macro + XI IED + Budget/Survey summary | Ramesh Singh cover-to-cover |
| Environment | Shankar IAS | Random PDF compilations |
| S&T | NCERT basics + current affairs | Engineering-level detail |
| Current affairs | One newspaper (≤1 h/day) + one monthly magazine | Several magazines, Telegram PDFs |
| CSAT | PYQ papers + R.S. Aggarwal for weak topics | A full quant course |

The full-time learner keeps the same list but adds Class XII Geography, the rest of Singhania, and Ramesh Singh's selected chapters.

## A working-professional week

| Slot | Task |
|---|---|
| Commute / lunch (20–30 min) | Current affairs only, from a daily summary or the monthly magazine |
| Mon–Fri 10:00–10:15 PM | Recall last night's chapter without opening the book |
| Mon–Fri 10:15–11:30 PM | Tonight's chapter (one normal chapter, or half of a long one) |
| Mon–Fri 11:30–12:00 | PYQs on exactly what was read |
| Saturday (7–8 h) | 3 h long/tough chapters · 2 h PYQs + short notes · 1.5 h CSAT · 1 h weekly current-affairs consolidation |
| Sunday 9:30–11:30 AM | Weekly test on the week's portion, at exam time |
| Sunday after | Mistake review, revision of this + last week, backlog; evening off |

Rules of the week: a drained night = 30 min of PYQs, never zero; public holidays become extra Saturdays; arrange 2–3 weeks of leave before Prelims now, not in May.

## A full-time day

| Slot | Task |
|---|---|
| 1 h | Newspaper (syllabus-relevant only) |
| 5 h | This week's subject, main reading |
| 1 h | PYQs on today's topic |
| 1 h | Revision of yesterday + last week |
| 30 min | CSAT on alternate days |
| Sunday | Weekly test + backlog |

## Ready-made 16-week calendar

`assets/plan-16-weeks-working-professional.json` holds a complete, fact-checked day-by-day 16-week plan (relative weeks, Mon–Sun) with real chapter names, a PYQ task and a study tip for each day, a weekly theme, 7 how-to-study rules per subject, and a 17-week CSAT Saturday track. Shape:

```
blocks[] = {key, name, dates, scope, howToStudy[], weeks[] = {week, theme, days[] = {day, task, pyq, tip}}}
```

Put calendar dates on it with the script for any learner (the chapter order and per-day sizing stay valid, only the calendar moves). Weeks are relative: week 1 starts on the learner's first Monday.

## Mains and optional (what to tell a Prelims-focused learner)

Decide the optional by the application form (usually Feb) because it must be declared there; don't study it before Prelims when Prelims is < 7 months away. Mains answer writing starts the day after Prelims. For a working professional, say plainly that Mains three months after Prelims is hard without leave, and plan for it after Prelims, not now.

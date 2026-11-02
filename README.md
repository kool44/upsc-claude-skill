# UPSC Prelims Mentor — a Claude skill

A complete preparation mentor for the UPSC Civil Services Examination (Prelims-first), packaged as a [Claude skill](https://support.claude.com/en/articles/12512180-using-skills-in-claude). Install it once and Claude becomes a single preparation room: it plans around *your* hours, tells you exactly which book and chapter to read (and what to skip), teaches the topic inside the chat, drills you with UPSC-style MCQs with real negative marking, clears doubts, and reviews your progress.

It is generic: any aspirant, any start date, any weekly hours, working professional or full-time.

## What it does

| You say | It does |
|---|---|
| "make me a plan till Prelims 2027, I can study 10 PM to 12 on weekdays" | Runs the calendar script, sizes foundation / revision / mock phases to your hours, gives a dated week table and tonight's first task |
| "which book for Polity, what can I skip" | Chapter-level table: priority, time, what UPSC asks, traps, skip list |
| "teach me Emergency Provisions" | Definition, basis, fact table, what UPSC asked, traps, check questions |
| "give me 10 economy MCQs" | UPSC-format statement questions, answers withheld, +2 / −0.667 scoring, verdict |
| "am I eligible, how many attempts" | Age and attempt rules by category, computed for your date of birth |
| "this news item" | Converts it into the static topic and the statement UPSC would make from it |
| "CSAT" | Diagnoses with a PYQ paper, fixes time management first |

## What's inside

```
upsc-prelims-mentor/
├── SKILL.md                      # how the mentor thinks and answers
├── references/
│   ├── exam-facts.md             # structure, marking, eligibility, failure patterns
│   ├── plan-template.md          # phases, weekly shapes, trimmed source list
│   ├── mcq-style.md              # UPSC question formats, scoring, elimination
│   ├── mcq-bank.json             # 99 verified MCQs across subjects
│   ├── polity.md                 # ┐
│   ├── modern-history.md         # │ one map per subject: weight → sources (use / skip)
│   ├── art-culture.md            # │ → chapter-by-chapter table (priority, time, what
│   ├── geography.md              # │ UPSC asks, traps) → data to memorise → how to
│   ├── economy.md                # │ teach → revision strategy → current-affairs hooks
│   ├── environment.md            # │
│   ├── science-tech.md           # │
│   ├── current-affairs.md        # │
│   └── csat.md                   # ┘
├── scripts/make_plan.py          # deterministic calendar: start, Prelims date, hours → phases and weeks
├── assets/plan-16-weeks-working-professional.json  # day-by-day foundation plan, relative weeks
└── evals/                        # three test prompts with graded assertions
```

The subject maps were generated and then independently fact-checked; corrections made during that pass are listed at the bottom of each file. Year-specific numbers (dates, vacancies, cutoffs) still change every year, and the skill is written to say so and point to upsc.gov.in.

## Install

**Claude.ai / Claude desktop:** download the `.skill` file from the latest release (or zip this folder), then Settings → Capabilities → Skills → upload.

**Claude Code:** copy the folder into your skills directory:

```bash
git clone https://github.com/<you>/upsc-prelims-mentor ~/.claude/skills/upsc-prelims-mentor
```

Then just talk about UPSC. The description is written so the skill triggers on Prelims, Mains, CSAT, Laxmikanth, NCERTs, PYQs, "which book", "teach me", "am I eligible", and timetable requests.

## Use the planner on its own

```bash
python3 scripts/make_plan.py --start 2026-11-02 --prelims 2027-05-23 --weekday-hours 2 --weekend-hours 7
python3 scripts/make_plan.py --start 2027-01-11 --prelims 2027-05-23 --weekday-hours 6 --weekend-hours 8 --json
```

It prints a Markdown week table (or JSON) with foundation / revision / mock phases, and warns when the syllabus does not fit the hours.

## Test it

Each folder under `evals/` is a realistic prompt with assertions in the layout `claude plugin eval` reads:

```bash
claude plugin eval . --allow-tools Write,Edit,Bash
```

In the first benchmark (3 prompts, with vs without the skill, double-graded), the skill passed 21/21 assertions against 20/21 for plain Claude, and answered about a third faster; the one baseline miss was an eligibility computation.

## Contributing

Corrections to facts are the most valuable contribution. Open an issue with the file, the line, the correct fact and the source (Constitution text, Laxmikanth edition and page, NCERT chapter, RBI/official site). Pull requests that add verified PYQ-mapped MCQs to `references/mcq-bank.json` are welcome; keep the `{topic, q, options[4], answer, explanation}` shape.

## Licence

MIT. Book titles are referenced for study guidance only; no copyrighted text is reproduced.

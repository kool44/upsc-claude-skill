# UPSC Mentor — a Claude skill for the whole Civil Services exam

A complete preparation mentor for the UPSC Civil Services Examination, from the first day of preparation to the Interview, packaged as a [Claude skill](https://support.claude.com/en/articles/12512180-using-skills-in-claude). Install it once and Claude becomes a single preparation room: it plans the whole cycle around *your* hours, tells you exactly which book and chapter to read (and what to skip), teaches the topic inside the chat, drills you with UPSC-style MCQs with real negative marking, grades your Mains answers and essays like an examiner, helps you choose and prepare the optional, runs mock interviews from your DAF, and reviews your progress.

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
| "check my GS2 answer" / "evaluate this essay" | Scores it against a rubric with a band, quotes what cost marks, rewrites the weakest section |
| "give me an ethics case study" | UPSC-style case, the structure, a 250-word model answer, the grading rubric |
| "which optional should I take, I'm an engineer" | Comparison by syllabus length, overlap and scoring consistency, a 2-week trial, a starter map |
| "mock interview, here is my DAF" | Builds the DAF question bank, then asks one question at a time and gives board-style feedback |
| "roadmap till the interview" | Stage-by-stage cycle from the planner script: foundation, Prelims mocks, 100-day Mains sprint, DAF, Interview |

## What's inside

```
upsc-mentor/
├── SKILL.md                      # how the mentor thinks and answers, mode by mode
├── references/
│   ├── exam-facts.md             # all three stages: structure, marking, eligibility, failure patterns
│   ├── roadmap.md                # the full cycle, three starting points, checkpoints
│   ├── plan-template.md          # Prelims phases, weekly shapes, trimmed source list
│   ├── mcq-style.md              # UPSC question formats, scoring, elimination
│   ├── mcq-bank.json             # 99 verified MCQs across subjects
│   ├── polity.md … csat.md       # Prelims maps, one per subject: sources (use / skip) →
│   │                             #   chapter table (priority, time, what UPSC asks, traps) →
│   │                             #   data to memorise → how to teach → revision → CA hooks
│   ├── mains-overview.md         # structure, what decides rank, Paper A/B, 100-day sprint
│   ├── gs1.md gs2.md gs3.md      # Mains GS maps: syllabus decoded → sources by topic →
│   ├── gs4-ethics.md             #   answer frameworks → data/examples → PYQ patterns → grading
│   ├── essay.md                  # topics 2013–2024, structure, examples bank, rubric
│   ├── answer-writing.md         # method, speed-building, templates, evaluation rubric
│   ├── optional-subjects.md      # choosing, comparison, starter maps for popular optionals
│   └── interview.md              # DAF as syllabus, 8–10 week plan, question types, mock protocol
├── scripts/
│   ├── make_roadmap.py           # start date, target year, hours → stage-by-stage cycle to Interview
│   └── make_plan.py              # start, Prelims date, hours → week-by-week Prelims calendar
├── assets/plan-16-weeks-working-professional.json  # day-by-day Prelims foundation plan, relative weeks
└── evals/                        # six test prompts with graded assertions
```

The subject maps and the Mains/Interview files were generated and then independently fact-checked; corrections made during that pass are listed at the bottom of each file. Year-specific numbers (dates, vacancies, cutoffs) still change every year, and the skill is written to say so and point to upsc.gov.in.

## Install

**Claude.ai / Claude desktop:** download the `.skill` file from the latest release (or zip this folder), then Settings → Capabilities → Skills → upload.

**Claude Code:** copy the folder into your skills directory:

```bash
git clone https://github.com/kool44/upsc-claude-skill ~/.claude/skills/upsc-mentor
```

Then just talk about UPSC. The description is written so the skill triggers on Prelims, Mains, CSAT, Laxmikanth, NCERTs, PYQs, "which book", "teach me", "am I eligible", and timetable requests.

## Use the planner on its own

```bash
python3 scripts/make_plan.py --start 2026-11-02 --prelims 2027-05-23 --weekday-hours 2 --weekend-hours 7
python3 scripts/make_plan.py --start 2027-01-11 --prelims 2027-05-23 --weekday-hours 6 --weekend-hours 8 --json
```

The roadmap script prints the stages from today to the Interview (foundation, Prelims mocks, Mains sprint, DAF, Interview) with dates, hours and done-when checkpoints, choosing the mode by months left (integrated Prelims+Mains, Prelims-first, or Prelims-only). The plan script prints the week-by-week Prelims calendar (or JSON) with foundation / revision / mock phases, and warns when the syllabus does not fit the hours.

## Test it

Each folder under `evals/` is a realistic prompt with assertions in the layout `claude plugin eval` reads:

```bash
claude plugin eval . --allow-tools Write,Edit,Bash
```

In the first benchmark (3 Prelims prompts, with vs without the skill, double-graded), the skill passed 21/21 assertions against 20/21 for plain Claude, and answered about a third faster; the one baseline miss was an eligibility computation. The second iteration added three Mains/Interview prompts (answer evaluation, ethics case study, DAF-based interview prep); results are in the repository's benchmark notes.

## Contributing

Corrections to facts are the most valuable contribution. Open an issue with the file, the line, the correct fact and the source (Constitution text, Laxmikanth edition and page, NCERT chapter, RBI/official site). Pull requests that add verified PYQ-mapped MCQs to `references/mcq-bank.json` are welcome; keep the `{topic, q, options[4], answer, explanation}` shape.

## Licence

MIT. Book titles are referenced for study guidance only; no copyrighted text is reproduced.

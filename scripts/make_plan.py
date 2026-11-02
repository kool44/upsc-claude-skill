#!/usr/bin/env python3
"""
make_plan.py — deterministic UPSC Prelims study calendar.

Given the learner's start date, Prelims date and weekly hours, it allocates the
foundation subjects, a revision phase and a mock phase to real calendar weeks,
and prints a Markdown calendar (or JSON with --json).

Usage:
  python3 make_plan.py --start 2026-11-02 --prelims 2027-05-23 \
      --weekday-hours 2 --weekend-hours 7 [--days-off 0] [--json]
  python3 make_plan.py --start 2027-01-11 --prelims 2027-05-23 --weekday-hours 6 --weekend-hours 8

Rules encoded here (why): a working professional gets ~27 h/week; the standard
one-source syllabus needs ~430 h of first reading, so 16 weeks at that pace.
The revision phase is fixed at ~6 weeks and the mock phase at ~7 weeks because
Prelims is decided by elimination skill built in mocks, not by first reading.
When time is short the script shrinks first reading, never the mock phase.
"""
import argparse, json, sys
from datetime import date, timedelta

# (key, name, share of foundation time, primary source)
SUBJECTS = [
    ("polity",      "Polity",                       3.0, "Laxmikanth, Indian Polity"),
    ("history",     "Modern History + Art & Culture",3.0, "Spectrum + selected Singhania"),
    ("geography",   "Geography",                    3.0, "NCERT XI (Physical + India) + atlas"),
    ("economy",     "Economy",                      3.0, "NCERT XII Macro + XI IED + Budget/Survey"),
    ("environment", "Environment",                  2.0, "Shankar IAS Environment"),
    ("scitech",     "Science & Tech + Ancient/Medieval (PYQ-driven)", 2.0, "NCERT basics + PYQs"),
]
FOUNDATION_HOURS = 380.0   # first reading of the trimmed syllabus (16 weeks at ~24 h/week)
REVISION_WEEKS_FULL = 6
MOCK_WEEKS_FULL = 7

def monday_on_or_before(d):
    return d - timedelta(days=d.weekday())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True, help="YYYY-MM-DD, first study day")
    ap.add_argument("--prelims", required=True, help="YYYY-MM-DD, Prelims date (assumed if not yet notified)")
    ap.add_argument("--weekday-hours", type=float, default=2.0, help="study hours per weekday")
    ap.add_argument("--weekend-hours", type=float, default=7.0, help="study hours per weekend day")
    ap.add_argument("--days-off", type=int, default=0, help="weekdays per week with zero study (e.g. shift work)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    start = date.fromisoformat(a.start)
    prelims = date.fromisoformat(a.prelims)
    if prelims <= start:
        sys.exit("Prelims date must be after start date")
    weekly = (5 - a.days_off) * a.weekday_hours + 2 * a.weekend_hours
    total_weeks = (prelims - start).days // 7
    notes = []

    # Phase sizing
    foundation_needed = FOUNDATION_HOURS / weekly if weekly else 0
    mock_w = min(MOCK_WEEKS_FULL, max(3, total_weeks // 4))
    revision_w = min(REVISION_WEEKS_FULL, max(2, total_weeks // 5))
    foundation_w = total_weeks - mock_w - revision_w
    if foundation_w < foundation_needed:
        notes.append(f"Only {foundation_w} weeks for first reading; the syllabus needs about "
                     f"{foundation_needed:.0f} weeks at {weekly:.0f} h/week. Trim sources further "
                     f"(PYQ-driven reading only for Art & Culture, Ancient/Medieval, S&T) and merge revision into reading.")
    if foundation_w < 6:
        notes.append("Fewer than 6 foundation weeks: treat this attempt as PYQ-and-mock driven. Read only Polity, Economy, Environment, Geography; everything else from PYQs.")
    if weekly < 20:
        notes.append(f"{weekly:.0f} h/week is below the ~25 h/week that a first full reading needs; protect weekends and plan 2-3 weeks of leave before Prelims.")

    # Allocate foundation weeks across subjects proportionally (largest remainder)
    total_share = sum(s[2] for s in SUBJECTS)
    raw = [(s, foundation_w * s[2] / total_share) for s in SUBJECTS]
    alloc = {s[0]: int(r) for s, r in raw}
    rem = foundation_w - sum(alloc.values())
    for s, r in sorted(raw, key=lambda x: -(x[1] - int(x[1]))):
        if rem <= 0: break
        alloc[s[0]] += 1; rem -= 1
    for s in SUBJECTS:
        if alloc[s[0]] == 0 and foundation_w > 0:
            notes.append(f"{s[1]} got 0 weeks: cover it only through PYQs and the chapter map's High-priority rows.")

    # Build calendar
    weeks = []
    cur = monday_on_or_before(start)
    wn = 1
    for s in SUBJECTS:
        for i in range(alloc[s[0]]):
            weeks.append({"week": wn, "from": cur.isoformat(), "to": (cur + timedelta(days=6)).isoformat(),
                          "phase": "Foundation", "subject": s[1], "key": s[0],
                          "focus": f"{s[3]} — part {i+1} of {alloc[s[0]]}",
                          "weekend": "Sat: long chapters + PYQs + 1.5h CSAT. Sun 9:30-11:30: weekly test, then mistake review + revision."})
            cur += timedelta(days=7); wn += 1
    for i in range(revision_w):
        weeks.append({"week": wn, "from": cur.isoformat(), "to": (cur + timedelta(days=6)).isoformat(),
                      "phase": "Revision", "subject": "All", "key": "revision",
                      "focus": f"2nd revision from short notes (pass {i+1}/{revision_w}); all PYQs subject-wise in one sitting; sectional tests",
                      "weekend": "Sat: sectional test + analysis. Sun: revision of weakest subject."})
        cur += timedelta(days=7); wn += 1
    for i in range(mock_w):
        weeks.append({"week": wn, "from": cur.isoformat(), "to": (cur + timedelta(days=6)).isoformat(),
                      "phase": "Mocks", "subject": "All", "key": "mocks",
                      "focus": "Full GS mock Sat + Sun at 9:30 AM; 1 CSAT mock/week; analyse each mock for as long as it took; 3rd/4th revision; 12-15 month current affairs compilation",
                      "weekend": "Mock, analysis, revision. Take leave in the final 2-3 weeks for daily mocks."})
        cur += timedelta(days=7); wn += 1

    out = {"start": start.isoformat(), "prelims": prelims.isoformat(), "weekly_hours": weekly,
           "weeks_total": total_weeks, "foundation_weeks": foundation_w, "revision_weeks": revision_w,
           "mock_weeks": mock_w, "allocation": alloc, "notes": notes, "weeks": weeks}
    if a.json:
        print(json.dumps(out, indent=1)); return

    print(f"# Study calendar: {start} → Prelims {prelims}\n")
    print(f"- Weekly hours: **{weekly:.0f}** · Weeks available: **{total_weeks}** · Foundation {foundation_w} wks · Revision {revision_w} wks · Mocks {mock_w} wks")
    for n in notes: print(f"- ⚠ {n}")
    print("\n| Wk | Dates | Phase | Subject | Focus |\n|---|---|---|---|---|")
    for w in weeks:
        print(f"| {w['week']} | {w['from']} → {w['to']} | {w['phase']} | {w['subject']} | {w['focus']} |")
    print("\nWeekend pattern: " + weeks[0]["weekend"] if weeks else "")

if __name__ == "__main__":
    main()

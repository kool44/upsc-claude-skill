#!/usr/bin/env python3
"""
make_roadmap.py — full-cycle UPSC CSE roadmap: Prelims → Mains → Interview.

Given today's date, the target exam year and weekly hours, it lays out the
phases from now to the Interview, with dates, hours and what gets done in each,
and prints Markdown (or JSON with --json). Use make_plan.py for the week-by-week
Prelims calendar inside the Prelims phase.

Usage:
  python3 make_roadmap.py --start 2026-11-02 --year 2027 --weekday-hours 2 --weekend-hours 7
  python3 make_roadmap.py --start 2026-01-10 --year 2027 --weekday-hours 6 --weekend-hours 8 --optional-started
  python3 make_roadmap.py --start 2026-11-02 --year 2027 --prelims 2027-05-23 --mains 2027-09-17 --json

Rules encoded here (why): the stages are sequential but preparation is not.
With > 12 months, GS is read once for both Prelims and Mains and the optional
gets its first reading before Prelims. With 7-12 months, GS reading stays
Mains-aware but the optional starts only if there are > 9 months. With < 7
months the plan is Prelims-only and everything else waits for the 100-day
Mains sprint after Prelims. Dates after the Prelims are typical UPSC calendar
positions; they are marked "assumed" and must be verified on upsc.gov.in.
"""
import argparse, json, sys
from datetime import date, timedelta

def typical(year):
    """Typical UPSC calendar positions (assumed until the notification confirms)."""
    return {
        "prelims": date(year, 5, 24),          # last Sunday of May, typically
        "prelims_result": date(year, 6, 14),
        "mains": date(year, 9, 17),            # mid/late September, typically
        "mains_result": date(year, 12, 10),
        "interview_start": date(year + 1, 1, 10),
        "interview_end": date(year + 1, 4, 15),
        "final_result": date(year + 1, 4, 30),
    }

def months_between(a, b):
    return (b - a).days / 30.44

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True, help="YYYY-MM-DD, today / first study day")
    ap.add_argument("--year", type=int, required=True, help="target CSE year (the year of the Prelims)")
    ap.add_argument("--prelims", help="YYYY-MM-DD if the Prelims date is known")
    ap.add_argument("--mains", help="YYYY-MM-DD if the Mains start date is known")
    ap.add_argument("--weekday-hours", type=float, default=2.0)
    ap.add_argument("--weekend-hours", type=float, default=7.0)
    ap.add_argument("--leave-weeks-before-prelims", type=int, default=2)
    ap.add_argument("--leave-weeks-before-mains", type=int, default=4)
    ap.add_argument("--optional-started", action="store_true", help="optional subject already chosen and started")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    start = date.fromisoformat(a.start)
    cal = typical(a.year)
    assumed = {"prelims": a.prelims is None, "mains": a.mains is None}
    if a.prelims: cal["prelims"] = date.fromisoformat(a.prelims)
    if a.mains: cal["mains"] = date.fromisoformat(a.mains)
    if cal["prelims"] <= start:
        sys.exit("Prelims date is not after the start date; use --year for the next cycle")

    weekly = 5 * a.weekday_hours + 2 * a.weekend_hours
    m_to_prelims = months_between(start, cal["prelims"])
    notes, phases = [], []

    def phase(name, frm, to, hours_per_week, focus, outputs):
        weeks = max(1, round((to - frm).days / 7))
        phases.append({"phase": name, "from": frm.isoformat(), "to": to.isoformat(), "weeks": weeks,
                       "hours_per_week": hours_per_week, "approx_hours": round(weeks * hours_per_week),
                       "focus": focus, "outputs": outputs})

    # --- Before Prelims -------------------------------------------------------
    optional_before = (m_to_prelims > 9) or a.optional_started
    if m_to_prelims >= 12:
        mode = "Integrated foundation (Prelims + Mains together), optional first reading before Prelims"
        split = start + timedelta(days=int((cal["prelims"] - start).days * 0.45))
        phase("Foundation: GS for Prelims and Mains, optional Paper I", start, split, weekly,
              "One source per GS subject read Mains-aware (add Mains-only topics: world history, post-independence, society, IR, internal security, disaster mgmt, ethics basics). Optional Paper I first reading in 30-40% of weekly hours. One answer a day from month 3; one essay a month.",
              ["GS first reading done with Mains notes (one page per topic)", "Optional Paper I read once with PYQs mapped", "Answer-writing habit: 1/day", "CSAT diagnosed"])
        phase("Prelims-focused: second reading, optional Paper II, tests", split, cal["prelims"] - timedelta(weeks=10), weekly,
              "GS revision for Prelims with PYQs, optional Paper II first reading (reduce to 25% of hours), sectional tests, answer writing drops to 3-4/week.",
              ["All PYQs 2011-" + str(a.year - 1) + " done subject-wise", "Optional both papers read once", "Sectional tests >= 60% accuracy"])
    elif m_to_prelims >= 7:
        mode = "Prelims-first with Mains-aware reading" + ("; optional starts now" if optional_before else "; optional after Prelims")
        split = start + timedelta(days=int((cal["prelims"] - start).days * 0.55))
        phase("Foundation: GS first reading (Mains-aware)", start, split, weekly,
              "One source per subject, PYQs after every chapter, one-page Mains notes per topic as you go." + (" Optional first reading in 25% of hours." if optional_before else " No optional yet."),
              ["GS first reading done", "Short notes per subject"] + (["Optional Paper I read once"] if optional_before else []))
        phase("Prelims-focused: revision and tests", split, cal["prelims"] - timedelta(weeks=10), weekly,
              "Second reading from notes, PYQs by subject in one sitting, sectional tests, CSAT weekly.",
              ["All PYQs done", "Sectional tests >= 60% accuracy", "CSAT mock >= 80/200"])
    else:
        mode = "Prelims-only (less than 7 months): optional and Mains wait for the post-Prelims sprint"
        notes.append("Fewer than 7 months to Prelims: do not start the optional or Mains answer writing now; declare the optional in the form (usually Feb) and start it the day after Prelims.")
        phase("Prelims foundation and revision", start, cal["prelims"] - timedelta(weeks=min(8, max(3, int(m_to_prelims * 4 // 3)))), weekly,
              "Use make_plan.py for the week-by-week calendar: trimmed one-source reading, PYQs after each chapter, revision from notes.",
              ["GS first reading done", "All PYQs done", "2 revisions"])
    leave_p = a.leave_weeks_before_prelims
    phase("Prelims mocks", phases[-1]["to"] and date.fromisoformat(phases[-1]["to"]), cal["prelims"], weekly + (20 if leave_p else 0),
          f"Full GS mock every weekend at 9:30 AM, CSAT mock weekly, analysis, 3rd/4th revision, 12-15 month current-affairs compilation. Take {leave_p} week(s) leave at the end if employed.",
          ["20+ full mocks analysed", "Accuracy on attempted >= 70%", "CSAT comfortably above 66.67"])

    # --- Prelims to Mains -----------------------------------------------------
    phase("Mains sprint (start the day after Prelims, do not wait for the result)", cal["prelims"] + timedelta(days=1), cal["mains"], weekly,
          "Week 1-2: optional revision/first reading if not done; week 3 onward: GS Mains-only topics, 10 answers/week rising to 20, 1 essay/week, ethics case studies, test series every 2 weeks, Paper A/B one weekend. "
          f"Take {a.leave_weeks_before_mains} weeks leave before Mains if employed." + (" Optional not started yet: give it 40% of hours in the first 8 weeks." if not optional_before else ""),
          ["Optional both papers revised", "6-8 full GS tests written", "8-10 essays written", "Value-addition notes per GS paper", "Paper A/B previous paper solved"])
    if cal["prelims_result"] < cal["mains"]:
        notes.append(f"Prelims result typically around {cal['prelims_result'].isoformat()} (assumed); by then 3 weeks of the Mains sprint should already be done.")

    # --- Mains to Interview ---------------------------------------------------
    phase("Mains to result: DAF-II and next-cycle hedge", cal["mains"] + timedelta(days=5), cal["mains_result"], max(10, weekly * 0.5),
          "Fill DAF-II carefully; start the DAF question bank; read the newspaper with opinions in mind; if the Mains attempt felt uncertain, restart Prelims revision for the next cycle in parallel.",
          ["DAF-II submitted", "200-question DAF bank drafted", "State/district fact sheet"])
    phase("Interview preparation", cal["mains_result"], cal["interview_end"], weekly,
          "DAF-based written answers, home state and district, 12-month current affairs with opinions, graduation and work linkage, 4-6 mock interviews, ethics/situational practice, body language.",
          ["6 mocks done with feedback", "Opinions on 40 contested issues written", "Service preferences justified"])

    if weekly < 20:
        notes.append(f"{weekly:.0f} h/week is thin for an integrated Prelims+Mains plan; protect weekends and plan leave before both Prelims and Mains.")
    if m_to_prelims < 12 and not optional_before:
        notes.append("The optional gets no reading before Prelims; the Mains sprint must give it 40% of hours for 8 weeks. Choose a short-syllabus optional with GS overlap (see references/optional-subjects.md).")
    assumed_note = "Dates after today are typical UPSC calendar positions (assumed) unless you passed --prelims/--mains; verify every date in the notification at upsc.gov.in."

    out = {"start": start.isoformat(), "target_year": a.year, "weekly_hours": weekly, "months_to_prelims": round(m_to_prelims, 1),
           "mode": mode, "calendar": {k: v.isoformat() for k, v in cal.items()}, "assumed": assumed, "phases": phases,
           "notes": notes + [assumed_note]}
    if a.json:
        print(json.dumps(out, indent=1)); return

    print(f"# UPSC CSE {a.year} roadmap: {start} → Interview (~{cal['interview_end']})\n")
    print(f"- Mode: **{mode}**")
    print(f"- Weekly hours: **{weekly:.0f}** · Months to Prelims: **{m_to_prelims:.1f}**")
    print(f"- Key dates{' (assumed)' if any(assumed.values()) else ''}: Prelims {cal['prelims']} · Mains {cal['mains']} · Interview {cal['interview_start']} to {cal['interview_end']} · Final result ~{cal['final_result']}")
    for n in out["notes"]: print(f"- ⚠ {n}")
    print("\n| Phase | From → To | Weeks | h/week | Focus | Done when |\n|---|---|---|---|---|---|")
    for p in phases:
        print(f"| {p['phase']} | {p['from']} → {p['to']} | {p['weeks']} | {p['hours_per_week']:.0f} | {p['focus']} | {'; '.join(p['outputs'])} |")
    print("\nNext: run scripts/make_plan.py for the week-by-week Prelims calendar inside the Prelims phases.")

if __name__ == "__main__":
    main()

# Problem
Validate whether a mission plan contains unsafe or non-compliant actions before execution.

# Solution
1. Save the mission text to a file (recommended), or pass it directly with `--text`.
2. Run:
   - `python /a0/instruments/default/mission_guard/mission_guard.py --file /path/to/mission.txt`
   - or `python /a0/instruments/default/mission_guard/mission_guard.py --text "your mission statement"`
3. Review flagged findings and update the plan until no `high` severity issues remain.

## 1. Create Skill File

- [x] 1.1 Create `.claude/skills/render-and-review/SKILL.md` with the skill header and purpose
- [x] 1.2 Write the input collection phase: use AskUserQuestion to gather model file path, change name, and plain-English model description from the user
- [x] 1.3 Write the render phase: run `uv run python render.py <model_file> <change_name>` via Bash; if it exits non-zero, report the failure and stop
- [x] 1.4 Write the review phase: read all four PNGs (`isometric.png`, `plan.png`, `front.png`, `side.png`) from `renders/<change_name>/` using the Read tool, then assess each view against the user-provided description
- [x] 1.5 Write the verdict output: produce per-view observations and an overall PASS or FAIL verdict with a brief explanation

## 2. Wire Up Shorthand Command

- [x] 2.1 Create `.claude/commands/render-and-review.md` as a shorthand that invokes the `render-and-review` skill

## 3. Smoke Test

- [x] 3.1 Invoke the skill with `models/cone.py`, change name `cone-review`, and description "a cone with its apex pointing upward and its circular base at the bottom, with a base radius of 10 and a height of 20"
- [x] 3.2 Confirm the skill surfaces the orientation issue identified earlier (apex appears at the bottom in current renders) and returns a FAIL verdict

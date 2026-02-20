## Context

The render harness (`render.py` + `blender_render.py`) verifies output by checking file existence only. We are adding a Claude Code skill that orchestrates the full pipeline: collect inputs from the user, run the render, then have Claude assess the rendered images using its native vision capability. This keeps everything within a Claude Code session — no external API calls, no new dependencies, no credentials to manage.

## Goals / Non-Goals

**Goals:**
- Provide a skill (`/render-and-review`) that runs the full render-then-review loop in one invocation
- Collect three inputs from the user: model file path, change name, and a written description of the expected model geometry
- Surface a clear pass/fail verdict with per-view observations after reviewing the renders
- Work entirely within the Claude Code session using the Bash and Read tools

**Non-Goals:**
- Not a headless/CI-compatible check (requires an interactive Claude Code session)
- Not a pixel-diff or perceptual hash comparison against a baseline
- Not a replacement for human review — the assessment is advisory
- Not modifying `render.py` or any existing Python scripts

## Decisions

### D1: Skill, not script

The review is implemented as a `.claude/skills/render-and-review/SKILL.md` file — a set of instructions Claude Code follows when the skill is invoked. Claude uses its existing Bash tool to run `render.py` and its Read tool to view the PNG outputs. No new code needs to be written or maintained.

**Alternative considered**: A standalone `review.py` script calling the Anthropic API. Rejected because it requires `ANTHROPIC_API_KEY` setup, adds the `anthropic` package as a dependency, and duplicates capability Claude Code already has natively.

### D2: User provides a written description upfront

The skill asks the user for a plain-English description of the model (e.g. "a cone, apex at the top, base radius 10, height 20") before running the render. This description becomes the ground truth for the review — Claude compares what it sees in the renders to what the description says.

**Alternative considered**: Deriving the description automatically from the model source. Rejected because parsing build123d code into a natural language description is fragile; a human-written description is more reliable and catches intent that may not be obvious from the code.

### D3: Skill reads all four PNGs after render

After `render.py` completes, the skill reads all four PNG files using the Read tool (which supports images natively in Claude Code). Claude then assesses each view against the description and gives an overall verdict.

### D4: Verdict is pass/fail with per-view observations

The skill outputs a structured assessment: a `PASS` or `FAIL` verdict, one observation per view, and an overall explanation. The format is human-readable prose — no JSON parsing needed since this is a human-in-the-loop tool.

### D5: Render failure halts the skill

If `render.py` exits non-zero, the skill reports the failure and stops — there are no images to review. The user is directed to fix the render error before re-invoking the skill.

## Risks / Trade-offs

- **Requires Claude Code session** → Cannot run in headless CI. Mitigation: this is acceptable; the skill is a developer-experience tool, not a CI gate.
- **Non-determinism** → Claude's assessment may vary across invocations. Mitigation: low-stakes advisory use; a human re-invokes if they disagree with the verdict.
- **LLM geometry limitations** → Claude reasons from rendered images, not STL geometry, and may miss subtle dimensional errors. Mitigation: scope the assessment to obvious failures (blank render, wrong shape family, severe inversion) rather than dimensional accuracy.

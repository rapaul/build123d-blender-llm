## Why

The render harness verifies that four PNG files exist after a Blender run, but does nothing to confirm their visual content is correct. A render could be blank, show an inverted model, or depict the wrong geometry without triggering any failure. Rather than building a separate script that calls the Anthropic API externally, we can close this gap with a Claude Code skill: the user provides a written description of what their model should look like, the skill runs the render pipeline, then Claude reviews the rendered images natively using its vision capability — no API key setup, no extra dependencies.

## What Changes

- Introduce a Claude Code skill (`render-and-review`) that orchestrates the full render-and-review loop in one invocation
- The skill collects the model file path, change name, and a user-written textual description of the model
- The skill runs `render.py` via Bash, then reads the four rendered PNGs and assesses them against the description
- The skill reports a clear pass/fail verdict with per-view observations

## Capabilities

### New Capabilities
- `render-and-review-skill`: A Claude Code skill that runs the render pipeline and then visually reviews the output images against a user-provided model description

### Modified Capabilities
(none)

## Impact

- New file: `.claude/skills/render-and-review/SKILL.md`
- No changes to `render.py`, `blender_render.py`, or `pyproject.toml`
- No new runtime dependencies
- Requires an active Claude Code session (not usable in headless CI)

## Why

Each render output directory contains model.py, model.stl, and four PNG images, but the textual prompt that drove the render is lost after the session ends. Capturing the prompt alongside other artifacts makes each `renders/<name>/` directory fully self-contained — all inputs and outputs in one place.

## What Changes

- The `render-and-review` skill writes the user-provided model description to `renders/<name>/prompt.txt` after collecting it, before running `render.py`

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `render-and-review-skill`: New requirement to persist the user-provided description as `renders/<name>/prompt.txt`

## Impact

- `.claude/skills/render-and-review.md` — skill updated to write prompt.txt using the Write tool
- `openspec/specs/render-and-review-skill/` — delta spec with new requirement
- No changes to `render.py`, `blender_render.py`, or any other scripts

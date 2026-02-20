## Why

When LLMs generate build123d models from textual descriptions, there is currently no way to verify that the generated geometry actually matches the intent — the model is code, not a visual artifact. A multi-view rendering harness closes this loop by producing canonical 2D images that an LLM (or human) can inspect to confirm correctness, and that can be re-run on every future change to catch regressions.

## What Changes

- New CLI-invocable render script that loads a build123d model and drives Blender headlessly to produce 4 views
- Four canonical camera positions: isometric (perspective overview), plan (top-down), front, and side (right)
- Renders saved as image files under `renders/<change-name>/` with predictable filenames (`isometric.png`, `plan.png`, `front.png`, `side.png`)
- Harness is designed to be invoked programmatically — usable as a validation step for any current or future build123d model change
- Convention established: every new model change should run the harness and store its renders before being considered complete

## Capabilities

### New Capabilities

- `render-harness`: Blender headless rendering pipeline that takes a build123d model file and a change name, produces 4 canonical view renders (isometric, plan, front, side), and stores them in a structured `renders/<change-name>/` output directory for AI-driven visual validation

### Modified Capabilities

(none)

## Impact

- **New dependency**: Blender must be installed and accessible via CLI (`blender --background`)
- **New files**: `render.py` (entrypoint), `renders/` output directory (gitignored or committed depending on workflow decision)
- **No changes** to existing build123d model code or project structure
- **LLM workflow**: Any agent generating or modifying a build123d model should invoke the harness and use the rendered images to verify output before finalising

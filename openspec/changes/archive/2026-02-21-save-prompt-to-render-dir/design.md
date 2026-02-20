## Context

The render-and-review skill already collects a model name and description from the user before running `render.py`. The render output directory (`renders/<name>/`) already contains `model.py`, `model.stl`, and four PNG images. The user's description (prompt) is currently discarded after the review step, making it impossible to recall what was intended when revisiting an old render folder.

## Goals / Non-Goals

**Goals:**
- Write the user-provided description to `renders/<name>/prompt.txt` so the directory is fully self-contained
- Keep the change minimal — no new scripts, no CLI changes

**Non-Goals:**
- Passing the prompt through `render.py` or `blender_render.py` as an argument
- Structured metadata formats (JSON, YAML) — plain text is sufficient
- Modifying the review output or verdict logic

## Decisions

**Where to write the file**: `renders/<name>/prompt.txt` — plain text, one file alongside the other artifacts. Consistent with the flat structure already in the directory.

**When to write**: After the user provides the description and before running `render.py`. This ensures the prompt is on disk even if the render fails, providing a record of intent.

**Who writes it**: The `render-and-review` skill itself, using the Write tool. No changes to `render.py` or `blender_render.py` are required. The skill already uses the Write tool (it reads image files via Read tool), so this is a natural fit.

**Alternatives considered**:
- Passing prompt as a CLI arg to `render.py`: would require changing the render harness CLI signature — more blast radius than needed for a simple file write.
- Writing after a successful render only: risks losing the prompt if the render fails; writing upfront is safer.

## Risks / Trade-offs

- [Risk] If the `renders/<name>/` directory doesn't exist yet when the skill tries to write `prompt.txt`, the Write tool may fail → Mitigation: write prompt.txt after `render.py` creates the directory (or ensure the skill creates the directory first). The simplest fix: write prompt.txt immediately after render.py succeeds (directory is guaranteed to exist), or use `mkdir -p` via Bash before writing.
- [Trade-off] Writing before rendering is safer for intent-capture but requires ensuring the output dir exists. Writing after rendering is simpler (dir always exists) but loses the prompt on render failure. Given the typical usage pattern (renders rarely fail after initial setup), writing after render is the pragmatic choice.

## Open Questions

- None — change is fully scoped.

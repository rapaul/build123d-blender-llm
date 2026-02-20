## Context

`render.py` currently exports the build123d shape to a `tempfile.NamedTemporaryFile`, passes the path to Blender, and deletes the file in a `finally` block once Blender exits. The STL is the canonical geometry output of the pipeline but is discarded before the user can access it.

## Goals / Non-Goals

**Goals:**
- Write the STL to `renders/<change-name>/model.stl` so it persists alongside the render images
- Remove the temp-file creation and cleanup logic

**Non-Goals:**
- Changing the tessellation tolerance (stays at 0.01 mm)
- Changing the Blender script interface (it still receives a path to an STL)
- Adding any STL post-processing or validation

## Decisions

### Write STL to output directory directly (not via temp then move)

Write the STL straight to `renders/<change-name>/model.stl` rather than writing to a temp file and moving it afterward.

**Rationale**: The output directory is created before anything else runs, so the path is always valid when the export happens. A direct write is simpler and avoids a copy/move step.

**Alternative considered**: Write to temp, then move into output dir after Blender succeeds. Rejected — unnecessary complexity; the file is only useful if rendering succeeded anyway, and keeping a partial STL on failure is not harmful.

### Filename: `model.stl` (fixed)

Use a fixed filename rather than deriving it from the model file name.

**Rationale**: Keeps the output directory structure predictable and easy to script against. The change name already provides uniqueness.

## Risks / Trade-offs

- **Existing renders/<change-name>/ directories**: Re-running render will overwrite `model.stl`. This is consistent with how render images are already handled (overwrite on re-run), so no new risk.
- **Disk space**: STL files for typical models are small (< 5 MB). Not a concern.

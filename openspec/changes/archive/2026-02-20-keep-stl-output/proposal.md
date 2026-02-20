## Why

The render harness currently deletes the STL file after Blender completes, treating it as a temporary artefact. The STL is in fact the primary geometry output of the process — it is the file a user would send to a slicer or fabricator — and should be retained alongside the render images.

## What Changes

- The STL file SHALL be written to the structured output directory (`renders/<change-name>/model.stl`) instead of a temporary location, and SHALL NOT be deleted after rendering.
- The Blender render script receives the STL path as before; no change to its interface is needed.
- The cleanup step that deletes the temporary STL is removed.

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `render-harness`: The geometry export requirement changes from "write to a temp file and delete after rendering" to "write to the output directory and keep the file as a permanent output artefact".

## Impact

- `render.py` — remove temp-file logic; write STL to `renders/<change-name>/model.stl`
- `openspec/specs/render-harness/spec.md` — the geometry export requirement is updated via a delta spec

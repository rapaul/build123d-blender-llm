# build123d-blender

Integrates [build123d](https://github.com/gumyr/build123d) (a Python CAD library) with Blender to produce multi-view renders for visual validation of generated geometry.

## Requirements

- **Python 3.10** (managed via `uv`)
- **Blender 4.x** — install from [blender.org/download](https://www.blender.org/download/) and ensure the `blender` binary is on your `PATH`

## Setup

```bash
uv sync
```

## Model file convention

Every build123d model file must assign its final shape to a top-level variable named **`result`**:

```python
from build123d import *

result = Box(10, 10, 10)
```

The render harness executes the model file in an isolated namespace and extracts `result` as the shape to render. If `result` is not defined, rendering will fail with a descriptive error.

## Rendering

```bash
uv run python render.py <model_file> <change_name>
```

Example:

```bash
uv run python render.py models/bracket.py my-bracket-v1
```

This produces four PNG renders under `renders/<change_name>/`:

| File | View |
|------|------|
| `isometric.png` | Isometric overview (azimuth 45°, elevation 35.264°) |
| `plan.png` | Top-down (orthographic, −Z axis) |
| `front.png` | Front view (orthographic, −Y axis) |
| `side.png` | Right side view (orthographic, −X axis) |

All renders use orthographic projection and are auto-fitted to the model's bounding box with a 10% margin.

## Blender binary location

The `render.py` script locates Blender in this order:

1. **`BLENDER_PATH` environment variable** — set this to the full path of the Blender executable if it is not on your system `PATH`:
   ```bash
   export BLENDER_PATH=/opt/blender-4.2/blender
   ```
2. **System `PATH`** — if `blender` is on your `PATH`, no configuration is needed.

If neither lookup succeeds, rendering exits with a helpful installation message.

## Output directory structure

```
renders/
  <change_name>/
    isometric.png
    plan.png
    front.png
    side.png
```

The `renders/` directory is committed to the repository so rendered images are versioned alongside the model code.

## Development workflow

This project uses **OpenSpec** for structured, spec-driven development. See `CLAUDE.md` for available `/opsx` commands.

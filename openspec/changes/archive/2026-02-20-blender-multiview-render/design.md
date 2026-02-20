## Context

build123d produces parametric 3D geometry via OpenCascade (OCC). Blender is a separate application with its own Python runtime. The two cannot share a process directly. To render a build123d model in Blender, geometry must cross a process boundary and a file format boundary.

The project currently has no rendering infrastructure — this design establishes the full pipeline from scratch.

## Goals / Non-Goals

**Goals:**
- Produce 4 reproducible renders (isometric, plan, front, side) for any given build123d model file
- Store renders in a predictable directory structure (`renders/<change-name>/`)
- Work headlessly (no GUI) via Blender's `--background` mode
- Be invokable with a single command: `uv run python render.py <model.py> <change-name>`
- Be reusable for any future build123d model change

**Non-Goals:**
- Interactive Blender UI or live preview
- Photorealistic rendering (fast, clean renders are sufficient)
- Diffing or comparing renders across changes (out of scope for this change)
- Supporting formats other than build123d Python files as input

## Decisions

### 1. STL as the geometry interchange format

build123d can export to STL via `Shape.export_stl()`. STL is universally importable in Blender without add-ons and is lossless enough for rendering purposes (mesh tessellation only, no material/colour data needed at this stage).

**Alternatives considered:**
- **STEP**: Requires a Blender add-on (e.g., `STEPper`) or external conversion — adds a fragile dependency
- **OBJ**: Viable, but STL is simpler (no material files) and better supported by build123d's export API
- **Direct OCC → Blender**: Would require running both runtimes in the same process — not possible

A temp STL file is written to disk, passed to Blender, then deleted after rendering.

### 2. Two-script architecture

The pipeline uses two scripts:

- **`render.py`** — runs in the standard `uv` Python environment. Responsible for: importing the model file, extracting the build123d shape, exporting to temp STL, invoking Blender as a subprocess.
- **`blender_render.py`** — runs inside Blender's embedded Python. Responsible for: importing the STL, setting up scene/cameras/lighting, rendering 4 views, saving output images.

Blender is invoked as:
```
blender --background --python blender_render.py -- <stl_path> <output_dir>
```

Arguments after `--` are passed through to the Blender Python script via `sys.argv`.

**Alternative considered:** A single script that does everything. Not possible — Blender's Python runtime is isolated and cannot import user packages (`build123d`, `uv`-managed deps).

### 3. Orthographic projection for all 4 views

All cameras use orthographic projection and are auto-fitted to the model's bounding box. This ensures renders are scale-consistent and unambiguous — orthographic views are standard for engineering/CAD validation.

**Isometric camera position**: azimuth 45°, elevation 35.264° (true isometric angles), orthographic. This is consistent with CAD conventions and easier for an LLM to reason about than an arbitrary perspective shot.

**Alternative considered:** Perspective projection for the isometric view (more "natural" look). Rejected — orthographic is more deterministic and better for geometric validation.

### 4. EEVEE render engine

Blender's EEVEE engine is used (not Cycles). EEVEE renders are near-instant headlessly, requires no GPU, and produces clean results for solid geometry with flat/studio lighting. Cycles would add significant render time with no benefit for this use case.

### 5. Camera auto-framing

Each camera is positioned relative to the model's bounding box centre and scaled to fit the model with a small margin. This keeps renders consistent regardless of model size or position in the scene.

### 6. Renders committed to the repository

`renders/` is committed, not gitignored. The renders are the primary validation artefacts — they should be versioned alongside the model code so any agent or human can inspect them. Each change overwrites its own named subdirectory.

## Risks / Trade-offs

- **Blender not on PATH** → Mitigation: `render.py` checks for `blender` binary at startup and exits with a clear error message pointing to installation instructions
- **STL tessellation loses fine detail** → Mitigation: use a fine tessellation tolerance in `export_stl()` (e.g., `0.01 mm`); acceptable for visual validation
- **Blender Python API version drift** → Mitigation: pin to Blender 4.x; document required version in README
- **Model file has side effects on import** → Mitigation: execute model in an isolated namespace; document that model files must expose a top-level `result` shape variable
- **Camera auto-framing produces inconsistent crops** if model origin is far from geometry → Mitigation: centre camera on bounding box midpoint, not world origin

## Open Questions

- Should `render.py` accept a `--blender-path` flag for systems where Blender is not on PATH? (Lean: yes, with `BLENDER_PATH` env var fallback)
- What variable name should model files export their shape as? (`result`? `shape`? `part`?) — needs to be documented as a convention
- Should renders be 800×800 or 1024×1024? Higher res is better for LLM vision models but slower

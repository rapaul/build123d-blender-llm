## 1. Project scaffolding

- [ ] 1.1 Create `renders/` directory with a `.gitkeep` so it is tracked by git
- [ ] 1.2 Verify `renders/` is absent from `.gitignore` (add an explicit comment if needed)
- [ ] 1.3 Create empty `render.py` and `blender_render.py` files at the project root

## 2. `render.py` — argument parsing and validation

- [ ] 2.1 Parse two positional CLI arguments: `<model_file>` and `<change_name>`; print usage to stderr and exit non-zero if either is missing
- [ ] 2.2 Validate that the model file path exists; exit with a clear error if not

## 3. `render.py` — model execution and shape extraction

- [ ] 3.1 Execute the model file in an isolated `exec()` namespace (not the current module namespace)
- [ ] 3.2 Extract the `result` variable from the namespace; exit with a descriptive error if it is missing
- [ ] 3.3 Handle exceptions raised during model execution: print traceback and exit non-zero

## 4. `render.py` — STL export

- [ ] 4.1 Export the extracted shape to a temporary STL file using `Shape.export_stl()` with tessellation tolerance `0.01`
- [ ] 4.2 Wrap the Blender invocation in a `try/finally` block that deletes the temp STL file on both success and failure

## 5. `render.py` — Blender binary detection

- [ ] 5.1 Check `BLENDER_PATH` environment variable first; fall back to locating `blender` on the system PATH via `shutil.which`
- [ ] 5.2 Exit with a non-zero status and a helpful installation message if neither lookup succeeds

## 6. `render.py` — Blender subprocess invocation

- [ ] 6.1 Construct output directory path as `<project_root>/renders/<change_name>/` and create it if absent
- [ ] 6.2 Invoke Blender as `blender --background --python blender_render.py -- <stl_path> <output_dir>` using `subprocess.run`
- [ ] 6.3 On non-zero Blender exit code, print Blender's stderr output and exit non-zero

## 7. `blender_render.py` — scene setup

- [ ] 7.1 Parse `sys.argv` after `--` to extract `stl_path` and `output_dir`
- [ ] 7.2 Delete all default scene objects (camera, cube, light) before importing
- [ ] 7.3 Import the STL file using `bpy.ops.import_mesh.stl(filepath=stl_path)`
- [ ] 7.4 Set the render engine to EEVEE (`bpy.context.scene.render.engine = "BLENDER_EEVEE"` or `"BLENDER_EEVEE_NEXT"` for Blender 4.2+)
- [ ] 7.5 Add a simple area light or sun lamp for flat studio illumination
- [ ] 7.6 Set render resolution to 1024×1024

## 8. `blender_render.py` — camera helper

- [ ] 8.1 Write a helper function `render_view(name, location, rotation, output_dir)` that: creates an orthographic camera, positions it at `location` with `rotation`, fits the orthographic scale to the model bounding box with a 10% margin, renders the scene, saves the result as `<name>.png` in `output_dir`, then deletes the camera
- [ ] 8.2 Compute model bounding box centre and max dimension from the imported mesh object to use in camera positioning and scale fitting

## 9. `blender_render.py` — four canonical renders

- [ ] 9.1 Render isometric view: camera at azimuth 45°, elevation 35.264° (true isometric), saved as `isometric.png`
- [ ] 9.2 Render plan view: camera looking straight down (−Z axis), saved as `plan.png`
- [ ] 9.3 Render front view: camera looking along −Y axis, saved as `front.png`
- [ ] 9.4 Render side view: camera looking along −X axis, saved as `side.png`

## 10. Convention documentation

- [ ] 10.1 Update `README.md` (or create one) documenting the `result` variable convention for model files
- [ ] 10.2 Document the `BLENDER_PATH` environment variable and the required Blender version (4.x)
- [ ] 10.3 Document the render invocation command and output directory structure

## 11. End-to-end verification

- [ ] 11.1 Create or use an existing simple build123d model file that exposes a `result` variable
- [ ] 11.2 Run `uv run python render.py <model.py> <change-name>` end-to-end and confirm all four PNG files are produced
- [ ] 11.3 Commit the render outputs to the repository

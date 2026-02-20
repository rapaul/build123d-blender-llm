## ADDED Requirements

### Requirement: CLI entrypoint accepts model file and change name
The system SHALL provide a `render.py` script invokable as `uv run python render.py <model.py> <change-name>` that orchestrates the full rendering pipeline.

#### Scenario: Valid invocation produces renders
- **WHEN** `render.py` is called with a valid model file path and a change name
- **THEN** it produces four image files (`isometric.png`, `plan.png`, `front.png`, `side.png`) under `renders/<change-name>/`

#### Scenario: Missing arguments
- **WHEN** `render.py` is called with fewer than two arguments
- **THEN** it exits with a non-zero status code and prints usage instructions to stderr

### Requirement: Model file imports and shape extraction
The system SHALL execute the model file in an isolated namespace and extract the top-level `result` variable as the build123d shape to render.

#### Scenario: Model exposes `result` variable
- **WHEN** the model file defines a top-level `result` variable holding a build123d `Shape`
- **THEN** `render.py` successfully extracts the shape for export

#### Scenario: Model file missing `result` variable
- **WHEN** the model file does not define a top-level `result` variable
- **THEN** `render.py` exits with a non-zero status code and prints a descriptive error message naming the missing variable

#### Scenario: Model file raises an exception on import
- **WHEN** the model file raises an exception during execution
- **THEN** `render.py` exits with a non-zero status code and prints the exception traceback

### Requirement: Geometry export to temporary STL
The system SHALL export the extracted build123d shape to a temporary STL file using a fine tessellation tolerance of 0.01 mm, and delete the file after Blender completes.

#### Scenario: Temporary STL is created before Blender is invoked
- **WHEN** `render.py` successfully extracts the shape
- **THEN** a temporary STL file exists on disk before the Blender subprocess is started

#### Scenario: Temporary STL is deleted after rendering
- **WHEN** the Blender subprocess exits (success or failure)
- **THEN** the temporary STL file is deleted from disk

### Requirement: Blender binary detection
The system SHALL locate the Blender binary via the `BLENDER_PATH` environment variable, falling back to `blender` on the system PATH, and exit with a clear error if neither is found.

#### Scenario: Blender found on PATH
- **WHEN** `blender` is available on the system PATH and `BLENDER_PATH` is not set
- **THEN** `render.py` uses the PATH `blender` binary without error

#### Scenario: BLENDER_PATH overrides PATH lookup
- **WHEN** `BLENDER_PATH` is set to a valid Blender executable path
- **THEN** `render.py` uses the path specified by `BLENDER_PATH`

#### Scenario: Blender not found
- **WHEN** `blender` is not on PATH and `BLENDER_PATH` is not set (or points to a missing file)
- **THEN** `render.py` exits with a non-zero status code and prints a message directing the user to install Blender

### Requirement: Blender invoked headlessly
The system SHALL invoke Blender as a subprocess using `--background` mode, passing the Blender render script and arguments after `--`.

#### Scenario: Blender subprocess command
- **WHEN** rendering is triggered
- **THEN** Blender is invoked as `blender --background --python blender_render.py -- <stl_path> <output_dir>` where `<output_dir>` is the absolute path to `renders/<change-name>/`

#### Scenario: Blender subprocess failure
- **WHEN** the Blender subprocess exits with a non-zero status code
- **THEN** `render.py` exits with a non-zero status code and surfaces the Blender stderr output

### Requirement: Four canonical orthographic renders
The Blender render script SHALL produce exactly four PNG images — `isometric.png`, `plan.png`, `front.png`, `side.png` — each using orthographic projection and auto-fitted to the model's bounding box.

#### Scenario: All four output files are created
- **WHEN** `blender_render.py` completes successfully
- **THEN** all four files (`isometric.png`, `plan.png`, `front.png`, `side.png`) exist in the output directory

#### Scenario: Isometric camera position
- **WHEN** the isometric view is rendered
- **THEN** the camera is placed at azimuth 45° and elevation 35.264° (true isometric angles) using orthographic projection

#### Scenario: Plan (top-down) camera position
- **WHEN** the plan view is rendered
- **THEN** the camera looks directly downward along the −Z axis using orthographic projection

#### Scenario: Front camera position
- **WHEN** the front view is rendered
- **THEN** the camera looks along the −Y axis using orthographic projection

#### Scenario: Side (right) camera position
- **WHEN** the side view is rendered
- **THEN** the camera looks along the −X axis using orthographic projection

### Requirement: Camera auto-framing to model bounding box
Each camera SHALL be positioned relative to the imported model's bounding box centre and scaled so the model fills the frame with a small margin, independent of model size or world origin.

#### Scenario: Model centred in all renders
- **WHEN** the model geometry is offset from the world origin
- **THEN** all four rendered images show the model centred, not clipped or cropped

#### Scenario: Small model and large model both fill the frame
- **WHEN** two models of very different sizes are rendered
- **THEN** both produce renders where the model occupies the majority of the image

### Requirement: EEVEE render engine
The system SHALL use Blender's EEVEE render engine for all renders to minimise render time and avoid GPU requirements.

#### Scenario: Engine is set to EEVEE
- **WHEN** `blender_render.py` configures the scene
- **THEN** `bpy.context.scene.render.engine` is set to `"BLENDER_EEVEE"` (or `"BLENDER_EEVEE_NEXT"` on Blender 4.2+)

### Requirement: Structured output directory
The system SHALL write renders to `renders/<change-name>/` relative to the project root, creating the directory if it does not exist, and overwrite any existing renders for the same change name.

#### Scenario: Output directory is created if absent
- **WHEN** `renders/<change-name>/` does not exist at render time
- **THEN** the directory is created before images are written

#### Scenario: Existing renders are overwritten
- **WHEN** `renders/<change-name>/` already contains render files from a previous run
- **THEN** the new renders replace the old ones without error

### Requirement: Renders committed to the repository
The `renders/` directory SHALL be committed to the repository (not gitignored) so rendered images are versioned alongside the model code.

#### Scenario: renders/ is not in .gitignore
- **WHEN** the project `.gitignore` is inspected
- **THEN** `renders/` is not listed as an ignored path

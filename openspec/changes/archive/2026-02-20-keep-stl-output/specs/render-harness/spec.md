## MODIFIED Requirements

### Requirement: Geometry export to output STL
The system SHALL export the extracted build123d shape to `renders/<change-name>/model.stl` using a fine tessellation tolerance of 0.01 mm. The file SHALL be retained after Blender completes and SHALL NOT be deleted.

#### Scenario: STL is written to the output directory
- **WHEN** `render.py` successfully extracts the shape
- **THEN** `renders/<change-name>/model.stl` exists on disk before the Blender subprocess is started

#### Scenario: STL persists after successful rendering
- **WHEN** the Blender subprocess exits with a zero status code
- **THEN** `renders/<change-name>/model.stl` still exists on disk

#### Scenario: STL persists after Blender failure
- **WHEN** the Blender subprocess exits with a non-zero status code
- **THEN** `renders/<change-name>/model.stl` still exists on disk

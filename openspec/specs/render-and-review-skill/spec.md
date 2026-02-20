# Render and Review Skill

## Purpose
Provides a Claude Code skill (`render-and-review`) that collects a model name and written model description from the user, runs the render pipeline against `models/<name>.py`, then visually reviews the four rendered PNGs against the description using Claude's native vision capability — no external API key or additional dependencies required.

## Requirements

### Requirement: Skill collects name and description before rendering
The skill SHALL prompt the user for a model name and a plain-English description of what the model should look like before running any commands. The model file path is derived as `models/<name>.py` and the render output directory as `renders/<name>/`.

#### Scenario: Inputs collected upfront
- **WHEN** the skill is invoked
- **THEN** it asks the user for the model name and a textual description of the expected model geometry before proceeding

#### Scenario: Name used to locate model file and output directory
- **WHEN** the user provides a model name
- **THEN** the skill runs `uv run python render.py models/<name>.py <name>` via the Bash tool

### Requirement: Render failure halts the skill
The skill SHALL stop and report the error if `render.py` exits with a non-zero status code.

#### Scenario: Render exits non-zero
- **WHEN** `render.py` exits with a non-zero status code
- **THEN** the skill reports the failure to the user and does not proceed to the review step

### Requirement: All four rendered images are read after a successful render
After a successful render, the skill SHALL read all four PNG files from `renders/<name>/` using the Read tool.

#### Scenario: Images read after successful render
- **WHEN** `render.py` exits with code 0
- **THEN** the skill reads `isometric.png`, `plan.png`, `front.png`, and `side.png` from `renders/<name>/`

### Requirement: Visual assessment compares renders to user description
The skill SHALL assess each rendered view against the user-provided description and produce a structured verdict.

#### Scenario: Per-view observations produced
- **WHEN** all four images have been read
- **THEN** the skill produces an observation for each view (isometric, plan, front, side) noting whether it is consistent with the description

#### Scenario: Overall pass/fail verdict produced
- **WHEN** per-view observations are complete
- **THEN** the skill produces an overall PASS or FAIL verdict with a brief explanation of the reasoning

### Requirement: Verdict communicated clearly to the user
The skill SHALL present the verdict and per-view observations in a readable format before finishing.

#### Scenario: PASS verdict output
- **WHEN** the renders are consistent with the description
- **THEN** the skill outputs a PASS verdict along with supporting observations for each view

#### Scenario: FAIL verdict output
- **WHEN** one or more renders are inconsistent with the description
- **THEN** the skill outputs a FAIL verdict and identifies which views failed and why

### Requirement: User description is persisted as prompt.txt in the render directory
After a successful render, the skill SHALL write the user-provided model description to `renders/<name>/prompt.txt` so that the render output directory is fully self-contained with all inputs and outputs.

#### Scenario: prompt.txt written after successful render
- **WHEN** `render.py` exits with code 0
- **THEN** the skill writes the user-provided description to `renders/<name>/prompt.txt` using the Write tool

#### Scenario: prompt.txt content matches user input exactly
- **WHEN** the user provides a description and the render succeeds
- **THEN** `renders/<name>/prompt.txt` contains exactly the text the user provided, with no modification or truncation

#### Scenario: prompt.txt not written if render fails
- **WHEN** `render.py` exits with a non-zero status code
- **THEN** the skill does NOT write `prompt.txt` and instead reports the render failure

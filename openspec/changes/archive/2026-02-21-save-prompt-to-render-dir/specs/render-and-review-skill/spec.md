## ADDED Requirements

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

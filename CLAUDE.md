# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`build123d-blender` is a Python project integrating [build123d](https://github.com/gumyr/build123d) (a Python CAD library) with Blender. It is currently in early bootstrap stage.

- **Python version**: 3.10 (pinned via `.python-version`)
- **Package manager**: [uv](https://docs.astral.sh/uv/)
- **Key dependency**: `build123d` (installed from git HEAD)

## Common Commands

```bash
# Install dependencies
uv sync

# Run the main entry point
uv run python main.py

# Run a specific script
uv run python <script.py>
```

## Development Workflow

This project uses **OpenSpec** for structured, spec-driven development with Claude Code. The workflow is available via `/opsx` commands:

- `/opsx:new` — Start a new change (creates artifacts: spec, tasks, etc.)
- `/opsx:ff` — Fast-forward through all artifact creation at once
- `/opsx:apply` — Implement tasks from a change
- `/opsx:continue` — Create the next artifact in a change
- `/opsx:verify` — Verify implementation matches artifacts
- `/opsx:archive` — Archive a completed change
- `/opsx:explore` — Think through ideas before starting a change
- `/opsx:sync` — Sync delta specs to main specs without archiving

OpenSpec change artifacts live under `.claude/` alongside the skill definitions.

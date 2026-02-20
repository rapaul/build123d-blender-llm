---
name: "Render and Review"
description: Render a build123d model and visually review the output images against a user-provided description
category: Workflow
tags: [render, review, build123d]
---

Render a build123d model and review the rendered images against a description.

1. Ask the user for the model name and a plain-English description of what it should look like.
2. Run `uv run python render.py models/<name>.py <name>` via the Bash tool.
3. If the render exits with a non-zero status code, report the error and stop.
4. After a successful render, use the Write tool to write the user-provided description (exactly as given) to `renders/<name>/prompt.txt`.
5. Read all four rendered images: `renders/<name>/isometric.png`, `renders/<name>/plan.png`, `renders/<name>/front.png`, `renders/<name>/side.png`.
6. Visually assess each image against the description, then produce a per-view observation and an overall PASS or FAIL verdict.

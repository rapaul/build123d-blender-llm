---
name: render-and-review
description: Render a build123d model and visually review the output images against a user-provided description. Use when the user wants to render a model and verify the renders look correct.
---

Render a build123d model and review the rendered images.

**Steps**

1. **Collect inputs from the user**

   Use the **AskUserQuestion tool** to ask for:

   - **Name**: The model name in kebab-case (e.g. `cone`). This is used as the change name and to locate the model file at `models/<name>.py`.
   - **Description**: A plain-English description of what the model should look like — shape, orientation, proportions (e.g. "a cone with apex pointing up, circular base at the bottom, base radius 10, height 20").

2. **Run the render pipeline**

   Run the following command via the Bash tool:
   ```
   uv run python render.py models/<name>.py <name>
   ```

   - If the command exits with a **non-zero status code**: report the error output to the user and **stop**.
   - If it exits with **code 0**: announce that rendering succeeded and proceed to review.

3. **Read the rendered images**

   Use the Read tool to read all four PNG files from `renders/<name>/`:
   - `renders/<name>/isometric.png`
   - `renders/<name>/plan.png`
   - `renders/<name>/front.png`
   - `renders/<name>/side.png`

4. **Assess each view against the description**

   For each view, compare what you see to the user's description. Consider:
   - Does the shape match (e.g. cone vs. cylinder vs. box)?
   - Is the orientation correct (e.g. apex up vs. down)?
   - Are there any anomalies (blank render, clipping, wrong geometry)?

5. **Output the verdict**

   Present a structured verdict:

   ```
   ## Render Review: <name>

   **Isometric**: <observation>
   **Plan (top-down)**: <observation>
   **Front**: <observation>
   **Side**: <observation>

   ---
   **Verdict: PASS** (or **FAIL**)
   <One sentence explanation>
   ```

   - **PASS**: All views are consistent with the description
   - **FAIL**: One or more views contradict the description — identify which and why

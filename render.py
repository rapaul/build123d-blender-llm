"""render.py — build123d multi-view render harness.

Usage:
    uv run python render.py <model_file> <change_name>

Loads a build123d model file, extracts the `result` shape, exports it to a
temporary STL, then invokes Blender headlessly to produce four canonical
renders (isometric, plan, front, side) under renders/<change_name>/.
"""

import os
import sys
import shutil
import subprocess
import tempfile
import traceback
from pathlib import Path

from build123d import export_stl


def find_blender() -> str:
    """Return path to Blender binary or exit with a helpful error."""
    blender_path = os.environ.get("BLENDER_PATH")
    if blender_path:
        if not Path(blender_path).is_file():
            print(
                f"Error: BLENDER_PATH is set to '{blender_path}' but the file does not exist.",
                file=sys.stderr,
            )
            sys.exit(1)
        return blender_path

    found = shutil.which("blender")
    if found:
        return found

    print(
        "Error: Blender not found.\n"
        "Install Blender 4.x and ensure 'blender' is on your PATH, or set the\n"
        "BLENDER_PATH environment variable to the full path of the blender executable.\n"
        "Download: https://www.blender.org/download/",
        file=sys.stderr,
    )
    sys.exit(1)


def main() -> None:
    # --- 2.1 Argument parsing ---
    if len(sys.argv) < 3:
        print(
            "Usage: uv run python render.py <model_file> <change_name>",
            file=sys.stderr,
        )
        sys.exit(1)

    model_file = Path(sys.argv[1])
    change_name = sys.argv[2]

    # --- 2.2 Validate model file exists ---
    if not model_file.exists():
        print(f"Error: model file not found: {model_file}", file=sys.stderr)
        sys.exit(1)

    # --- 3.1 Execute model in isolated namespace ---
    namespace: dict = {}
    try:
        with open(model_file, "r") as f:
            source = f.read()
        exec(compile(source, str(model_file), "exec"), namespace)  # noqa: S102
    except Exception:
        # --- 3.3 Handle exceptions during model execution ---
        print(f"Error: exception while executing model file '{model_file}':", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

    # --- 3.2 Extract `result` variable ---
    shape = namespace.get("result")
    if shape is None:
        print(
            f"Error: model file '{model_file}' did not define a top-level 'result' variable.\n"
            "Make sure your model file assigns the final build123d shape to 'result'.",
            file=sys.stderr,
        )
        sys.exit(1)

    # --- 5.1 / 5.2 Locate Blender binary ---
    blender_bin = find_blender()

    # --- 6.1 Construct output directory ---
    project_root = Path(__file__).parent
    output_dir = project_root / "renders" / change_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- 4.1 Export to temporary STL ---
    tmp_stl = tempfile.NamedTemporaryFile(suffix=".stl", delete=False)
    tmp_stl.close()
    tmp_stl_path = Path(tmp_stl.name)

    try:
        export_stl(shape, str(tmp_stl_path), tolerance=0.01)

        # --- 6.2 Invoke Blender subprocess ---
        blender_script = project_root / "blender_render.py"
        cmd = [
            blender_bin,
            "--background",
            "--python", str(blender_script),
            "--",
            str(tmp_stl_path),
            str(output_dir.resolve()),
        ]
        # Note: Blender 4.2+ supports --gpu-backend none for GPU-free environments.
        # We rely on blender_render.py falling back to Cycles CPU if EEVEE is unavailable.
        env = os.environ.copy()
        # Use software Mesa rendering on GPU-free / WSL2 environments
        env.setdefault("LIBGL_ALWAYS_SOFTWARE", "1")
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)

        # Always surface Blender's output for debugging
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)

        # --- 6.3 Handle Blender failure ---
        if result.returncode != 0:
            print("Error: Blender exited with a non-zero status.", file=sys.stderr)
            sys.exit(result.returncode)

        # Verify expected output files were produced
        expected = ["isometric.png", "plan.png", "front.png", "side.png"]
        missing = [f for f in expected if not (output_dir / f).exists()]
        if missing:
            print(
                f"Error: Blender exited successfully but the following renders are missing: {missing}",
                file=sys.stderr,
            )
            sys.exit(1)

    finally:
        # --- 4.2 Delete temp STL on success or failure ---
        if tmp_stl_path.exists():
            tmp_stl_path.unlink()

    print(f"Renders written to: {output_dir}")


if __name__ == "__main__":
    main()

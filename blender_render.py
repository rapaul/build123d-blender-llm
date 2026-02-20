"""blender_render.py — Blender-internal render script for build123d models.

Runs inside Blender's embedded Python environment.

Usage (invoked by render.py via subprocess):
    blender --background --python blender_render.py -- <stl_path> <output_dir>

Produces four PNG renders in <output_dir>:
    isometric.png, plan.png, front.png, side.png
"""

import sys
import math
from pathlib import Path

import bpy
import mathutils


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args() -> tuple[str, str]:
    """Extract stl_path and output_dir from sys.argv after '--'."""
    argv = sys.argv
    try:
        sep = argv.index("--")
    except ValueError:
        print("Error: expected '--' separator in argv", file=sys.stderr)
        sys.exit(1)
    args = argv[sep + 1:]
    if len(args) < 2:
        print("Error: expected <stl_path> <output_dir> after '--'", file=sys.stderr)
        sys.exit(1)
    return args[0], args[1]


# ---------------------------------------------------------------------------
# Scene setup
# ---------------------------------------------------------------------------

def clear_scene() -> None:
    """Delete all default scene objects (camera, cube, light, etc.)."""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def import_stl(stl_path: str) -> bpy.types.Object:
    """Import an STL file and return the imported mesh object."""
    bpy.ops.object.select_all(action="DESELECT")
    try:
        # Blender 4.x preferred API
        bpy.ops.wm.stl_import(filepath=stl_path)
    except AttributeError:
        # Older Blender API
        bpy.ops.import_mesh.stl(filepath=stl_path)
    imported = bpy.context.selected_objects
    if not imported:
        print(f"Error: no objects imported from {stl_path}", file=sys.stderr)
        sys.exit(1)
    return imported[0]


def setup_render_engine() -> None:
    """Configure the render engine.

    Preference order:
    1. BLENDER_EEVEE_NEXT (Blender 4.2–4.x)
    2. BLENDER_EEVEE     (Blender 4.0–4.1, 5.0+)
    3. CYCLES            (CPU fallback for headless/GPU-free environments)
    """
    scene = bpy.context.scene
    for engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            scene.render.engine = engine
            if scene.render.engine == engine:
                print(f"Render engine: {engine}")
                return
        except TypeError:
            continue

    # Fall back to Cycles CPU — works headlessly without GPU or OpenGL
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    print("Render engine: CYCLES (CPU fallback)")


def setup_lighting() -> None:
    """Add a sun lamp for flat studio illumination."""
    bpy.ops.object.light_add(type="SUN", location=(5, 5, 10))
    sun = bpy.context.object
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(45), 0, math.radians(45))


def setup_resolution() -> None:
    """Set render resolution to 1024×1024."""
    scene = bpy.context.scene
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.resolution_percentage = 100
    # Use a light background for cleaner CAD renders
    scene.world.color = (0.9, 0.9, 0.9)


# ---------------------------------------------------------------------------
# Bounding box helpers
# ---------------------------------------------------------------------------

def get_bbox_info(obj: bpy.types.Object) -> tuple:
    """Return (center, dx, dy, dz, max_dim) in world space."""
    corners = [obj.matrix_world @ mathutils.Vector(v) for v in obj.bound_box]
    xs = [v.x for v in corners]
    ys = [v.y for v in corners]
    zs = [v.z for v in corners]

    center = mathutils.Vector((
        (min(xs) + max(xs)) / 2,
        (min(ys) + max(ys)) / 2,
        (min(zs) + max(zs)) / 2,
    ))
    dx = max(xs) - min(xs)
    dy = max(ys) - min(ys)
    dz = max(zs) - min(zs)
    max_dim = max(dx, dy, dz, 0.001)  # guard against degenerate geometry
    return center, dx, dy, dz, max_dim


# ---------------------------------------------------------------------------
# Camera helper
# ---------------------------------------------------------------------------

def render_view(
    name: str,
    cam_offset_dir: mathutils.Vector,
    ortho_scale: float,
    center: mathutils.Vector,
    max_dim: float,
    output_dir: str,
    up_axis: str = "Z",
) -> None:
    """Create an orthographic camera, render one view, save <name>.png, delete camera.

    Args:
        name:           Output filename stem (e.g. "isometric").
        cam_offset_dir: Normalised vector from model centre toward camera position.
        ortho_scale:    Orthographic scale (world units visible across the frame).
        center:         Bounding box centre of the model.
        max_dim:        Largest bounding box dimension (used for clip distance).
        output_dir:     Directory where <name>.png is written.
        up_axis:        World axis used as camera up ('Y' or 'Z').
    """
    scene = bpy.context.scene

    # Position camera far enough to avoid near-clipping
    distance = max_dim * 20
    cam_location = center + cam_offset_dir * distance

    # Rotation: make camera's -Z axis point toward model centre
    look_dir = (center - cam_location).normalized()
    rot_quat = look_dir.to_track_quat("-Z", up_axis)

    # Create camera
    cam_data = bpy.data.cameras.new(name=f"cam_{name}")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = ortho_scale
    cam_data.clip_start = 0.1
    cam_data.clip_end = distance * 3

    cam_obj = bpy.data.objects.new(f"cam_{name}", cam_data)
    scene.collection.objects.link(cam_obj)
    cam_obj.location = cam_location
    cam_obj.rotation_euler = rot_quat.to_euler()
    scene.camera = cam_obj

    # Render and save
    output_path = str(Path(output_dir) / f"{name}.png")
    scene.render.filepath = output_path
    scene.render.image_settings.file_format = "PNG"
    scene.render.use_file_extension = False
    bpy.ops.render.render(write_still=True)

    print(f"  Saved: {output_path}")

    # Clean up this camera
    bpy.data.objects.remove(cam_obj)
    bpy.data.cameras.remove(cam_data)


# ---------------------------------------------------------------------------
# Four canonical renders
# ---------------------------------------------------------------------------

def render_all_views(center: mathutils.Vector, dx: float, dy: float, dz: float, max_dim: float, output_dir: str) -> None:
    """Render isometric, plan, front, and side views."""
    margin = 1.1

    # 9.1 Isometric: azimuth 45°, elevation 35.264° (true isometric)
    az = math.radians(45)
    el = math.radians(35.264)
    iso_dir = mathutils.Vector((
        math.cos(el) * math.cos(az),
        math.cos(el) * math.sin(az),
        math.sin(el),
    )).normalized()
    render_view(
        "isometric",
        iso_dir,
        max_dim * margin,
        center, max_dim, output_dir,
        up_axis="Z",
    )

    # 9.2 Plan: camera above, looking straight down (−Z axis)
    render_view(
        "plan",
        mathutils.Vector((0.0, 0.0, 1.0)),
        max(dx, dy, 0.001) * margin,
        center, max_dim, output_dir,
        up_axis="Y",
    )

    # 9.3 Front: camera at +Y, looking along −Y axis
    render_view(
        "front",
        mathutils.Vector((0.0, 1.0, 0.0)),
        max(dx, dz, 0.001) * margin,
        center, max_dim, output_dir,
        up_axis="Z",
    )

    # 9.4 Side: camera at +X, looking along −X axis
    render_view(
        "side",
        mathutils.Vector((1.0, 0.0, 0.0)),
        max(dy, dz, 0.001) * margin,
        center, max_dim, output_dir,
        up_axis="Z",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    stl_path, output_dir = parse_args()

    print(f"blender_render.py: STL={stl_path}, output={output_dir}")

    clear_scene()

    print("Importing STL...")
    obj = import_stl(stl_path)

    setup_render_engine()
    setup_lighting()
    setup_resolution()

    center, dx, dy, dz, max_dim = get_bbox_info(obj)
    print(f"Model bbox: dx={dx:.3f}, dy={dy:.3f}, dz={dz:.3f}, centre={center}")

    print("Rendering views...")
    render_all_views(center, dx, dy, dz, max_dim, output_dir)

    print("blender_render.py: done.")


try:
    main()
except SystemExit:
    raise
except Exception:
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

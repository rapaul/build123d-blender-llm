"""A dice modeled with build123d.

5cm cube with indented circular pips on each face (1–6).
Standard die layout: opposite faces sum to 7.

Exposes a `result` variable as required by render.py.
"""

from build123d import *

size = 50  # 5cm cube
pip_r = 3.5  # pip radius in mm
pip_depth = 2  # pip indentation depth in mm
spacing = 12  # pip spacing from center in mm
half = size / 2

# Pip 2D patterns (u, v) relative to face center
pip_positions = {
    1: [(0, 0)],
    2: [(-spacing, -spacing), (spacing, spacing)],
    3: [(-spacing, -spacing), (0, 0), (spacing, spacing)],
    4: [(-spacing, -spacing), (-spacing, spacing), (spacing, -spacing), (spacing, spacing)],
    5: [(-spacing, -spacing), (-spacing, spacing), (0, 0), (spacing, -spacing), (spacing, spacing)],
    6: [
        (-spacing, -spacing), (-spacing, 0), (-spacing, spacing),
        (spacing, -spacing), (spacing, 0), (spacing, spacing),
    ],
}

with BuildPart() as part:
    Box(size, size, size)

    # +Z face = 1 pip
    for u, v in pip_positions[1]:
        with BuildSketch(Plane.XY.offset(half)):
            with Locations([(u, v)]):
                Circle(pip_r)
        extrude(amount=-pip_depth, mode=Mode.SUBTRACT)

    # -Z face = 6 pips
    for u, v in pip_positions[6]:
        with BuildSketch(Plane.XY.offset(-half)):
            with Locations([(u, v)]):
                Circle(pip_r)
        extrude(amount=pip_depth, mode=Mode.SUBTRACT)

    # +X face = 2 pips
    for u, v in pip_positions[2]:
        with BuildSketch(Plane.YZ.offset(half)):
            with Locations([(u, v)]):
                Circle(pip_r)
        extrude(amount=-pip_depth, mode=Mode.SUBTRACT)

    # -X face = 5 pips
    for u, v in pip_positions[5]:
        with BuildSketch(Plane.YZ.offset(-half)):
            with Locations([(u, v)]):
                Circle(pip_r)
        extrude(amount=pip_depth, mode=Mode.SUBTRACT)

    # +Y face = 3 pips
    for u, v in pip_positions[3]:
        with BuildSketch(Plane.XZ.offset(half)):
            with Locations([(u, v)]):
                Circle(pip_r)
        extrude(amount=-pip_depth, mode=Mode.SUBTRACT)

    # -Y face = 4 pips
    for u, v in pip_positions[4]:
        with BuildSketch(Plane.XZ.offset(-half)):
            with Locations([(u, v)]):
                Circle(pip_r)
        extrude(amount=pip_depth, mode=Mode.SUBTRACT)

result = part.part

"""A simple cone modeled with build123d.

Exposes a `result` variable as required by render.py.
"""

from build123d import *

result = Cone(bottom_radius=10, top_radius=0, height=20)

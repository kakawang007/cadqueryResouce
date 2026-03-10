"""Shared parameters for hexagonal drawer system.

Extracted from cadquery-contrib/hexagonal_drawers/base.py module-level variables.
These are used across multiple storage modules (frame, drawer, organisers).
"""

from types import SimpleNamespace


#: Outside diameter of the hexagonal drawer frame (mm).
HEX_DIAM = 80

#: Wall thickness (mm).
WALL_THICK = 3

#: Clearance specifications.
CLEARANCE = SimpleNamespace(tight=0.3)
CLEARANCE.loose = CLEARANCE.tight * 2

#: Drawer length (mm).
DRAWER_LENGTH = 150

#: Minimum thickness of dovetail joint (mm).
DOVETAIL_MIN_THICK = WALL_THICK * 2

#: Frame Y dimension (total length including walls and clearance).
FRAME_Y = DRAWER_LENGTH + CLEARANCE.loose + 2 * WALL_THICK


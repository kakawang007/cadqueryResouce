"""Hexagonal drawer with handle.

Migrated from cadquery-contrib/hexagonal_drawers/base.py (drawer part).
"""

import cadquery as cq

from cq_models.base import CqWorkplaneModel
from cq_models.storage.params import (
    HEX_DIAM, WALL_THICK, CLEARANCE, DRAWER_LENGTH, FRAME_Y,
)


class HexagonalDrawer(CqWorkplaneModel):
    """Hexagonal drawer that fits inside the HexagonalFrame.

    :param hex_diam: Outside diameter of the parent frame (mm).
    :param wall_thick: Wall thickness (mm).
    :param drawer_length: Drawer depth (mm).
    :param frame_y: Parent frame Y dimension (mm).
    """

    def __init__(
        self,
        hex_diam: float = HEX_DIAM,
        wall_thick: float = WALL_THICK,
        drawer_length: float = DRAWER_LENGTH,
        frame_y: float = FRAME_Y,
    ) -> None:
        self.hex_diam = hex_diam
        self.wall_thick = wall_thick
        self.drawer_length = drawer_length
        self.frame_y = frame_y
        self._cq_object = self._make()

    def _make_frame_shell(self) -> cq.Workplane:
        """Create the parent frame shell (used to derive drawer shape)."""
        return (
            cq.Workplane("XZ")
            .polygon(6, self.hex_diam)
            .extrude(self.frame_y)
            .faces("<Y")
            .shell(-2 * self.wall_thick)
        )

    def _make(self) -> cq.Workplane:
        frame = self._make_frame_shell()

        drawer = (
            frame
            .faces("<Y[1]")
            .wires()
            .translate((0, -CLEARANCE.loose, 0))
            .toPending()
            .offset2D(-CLEARANCE.loose)
            .extrude(self.drawer_length, combine=False)
            .faces(">Z or >>Z[-2]")
            .shell(-self.wall_thick)
        )

        # Build the handle
        handle = drawer.faces("<Y").edges("<Z")
        handle_width = handle.val().Length()
        handle = (
            handle
            .workplane(centerOption="CenterOfMass")
            .transformed(rotate=(-90, 0, 180))
            .circle(handle_width / 2)
            .circle(handle_width / 2 - self.wall_thick)
            .transformed(rotate=(30, 0, 0))
            .extrude(self.hex_diam / 2, combine=False)
            .newObject([drawer.faces("<Y").val()])
            .workplane(centerOption="CenterOfMass")
            .split(keepTop=True)
        )

        drawer = drawer.union(handle)
        return drawer


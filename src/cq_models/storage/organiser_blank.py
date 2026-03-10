"""Blank organiser that takes up 1/3 of a drawer.

Migrated from cadquery-contrib/hexagonal_drawers/organiser_blank.py.
"""

import cadquery as cq

from cq_models.base import CqWorkplaneModel
from cq_models.storage.hexagonal_drawer import HexagonalDrawer
from cq_models.storage.params import CLEARANCE, DRAWER_LENGTH


class OrganiserBlank(CqWorkplaneModel):
    """Blank organiser insert that fills 1/3 of a hexagonal drawer.

    This serves as a base shape for specialised organisers
    (collet organiser, bit organiser, etc.).

    :param drawer_length: Drawer depth (mm).
    """

    def __init__(self, drawer_length: float = DRAWER_LENGTH) -> None:
        self.drawer_length = drawer_length
        self._cq_object = self._make()

    def _make(self) -> cq.Workplane:
        drawer_obj = HexagonalDrawer().cq_object

        # Grab the inner profile of the drawer
        lines = (
            drawer_obj
            .faces(">Y")
            .workplane(offset=-self.drawer_length / 2)
            .section()
            .edges()
            .vals()
        )
        assert len(lines) == 8

        # Sort lines by radius about Y axis
        lines.sort(
            key=lambda x: cq.Vector(x.Center().x, 0, x.Center().z).Center().Length
        )
        wire = cq.Wire.assembleEdges(lines[0:3])
        wire = cq.Wire.combine(
            [wire, cq.Edge.makeLine(wire.endPoint(), wire.startPoint())]
        )[0]
        wire_center = wire.Center()
        wire = wire.translate(cq.Vector(0, -wire_center.y, 0))

        organiser = (
            cq.Workplane("XZ")
            .newObject([wire])
            .toPending()
            .extrude(self.drawer_length / 3 - CLEARANCE.loose)
        )
        return organiser


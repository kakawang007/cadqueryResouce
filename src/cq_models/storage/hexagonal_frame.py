"""Hexagonal drawer frame with dovetail joints.

Migrated from cadquery-contrib/hexagonal_drawers/base.py (frame part).
"""

from math import tan, radians

import cadquery as cq

from cq_models.base import CqWorkplaneModel
from cq_models.storage.params import (
    HEX_DIAM, WALL_THICK, CLEARANCE, DOVETAIL_MIN_THICK, FRAME_Y,
)


class HexagonalFrame(CqWorkplaneModel):
    """Hexagonal drawer frame with dovetail joints for stacking.

    :param hex_diam: Outside diameter of the hexagonal frame (mm).
    :param wall_thick: Wall thickness (mm).
    :param frame_y: Frame depth / Y dimension (mm).
    """

    def __init__(
        self,
        hex_diam: float = HEX_DIAM,
        wall_thick: float = WALL_THICK,
        frame_y: float = FRAME_Y,
    ) -> None:
        self.hex_diam = hex_diam
        self.wall_thick = wall_thick
        self.frame_y = frame_y
        self._cq_object = self._make()

    def _make(self) -> cq.Workplane:
        frame = (
            cq.Workplane("XZ")
            .polygon(6, self.hex_diam)
            .extrude(self.frame_y)
            .faces("<Y")
            .shell(-2 * self.wall_thick)
        )

        top_length = frame.faces(">Z").val().BoundingBox().ylen
        dovetail_base_radius = frame.faces("<Y").edges(">Z").val().Center().z
        dovetail_length = 0.9 * top_length

        # Make the male dovetail joint
        dovetail_positive = (
            cq.Workplane()
            .hLine(DOVETAIL_MIN_THICK / 2)
            .line(self.wall_thick * tan(radians(30)), self.wall_thick)
            .hLineTo(0)
            .mirrorY()
            .extrude(-dovetail_length)
            .faces("<Z")
            .edges("<Y")
            .workplane()
            .transformed(rotate=(60, 0, 0))
            .split(keepBottom=True)
        )

        # Make the female dovetail (with clearance)
        dovetail_negative = (
            dovetail_positive
            .tag("dovetail_positive")
            .faces(">Z")
            .wires()
            .toPending()
            .offset2D(CLEARANCE.tight)
            .faces(">Z", tag="dovetail_positive")
            .workplane()
            .extrude(-(dovetail_length + CLEARANCE.tight))
            .faces("<Z")
            .edges("<Y")
            .workplane()
            .transformed(rotate=(60, 0, 0))
            .split(keepBottom=True)
            .mirror("XZ")
        )

        dovetail_baseplane = (
            frame.faces("<Y").workplane(centerOption="CenterOfMass")
        )
        dovetail_positive = (
            dovetail_baseplane
            .polarArray(dovetail_base_radius, startAngle=-60, angle=120, count=3)
            .eachpoint(
                lambda loc: dovetail_positive.val().located(loc),
                useLocalCoordinates=True,
            )
        )
        dovetail_negative = (
            dovetail_baseplane
            .polarArray(dovetail_base_radius, startAngle=120, angle=120, count=3)
            .eachpoint(
                lambda loc: dovetail_negative.val().located(loc),
                useLocalCoordinates=True,
            )
        )

        frame = frame.union(dovetail_positive, glue=True).cut(dovetail_negative)
        return frame


"""Organiser for cutters with a 3.125mm shank.

Migrated from cadquery-contrib/hexagonal_drawers/organiser_3_125_bits.py.
"""

import cadquery as cq

from cq_models.base import CqWorkplaneModel
from cq_models.storage.organiser_blank import OrganiserBlank
from cq_models.storage.params import CLEARANCE, WALL_THICK


class BitOrganiser(CqWorkplaneModel):
    """Organiser insert with holes for 3.125mm shank cutters.

    :param shank_diam: Shank diameter of the cutters (mm).
    """

    def __init__(self, shank_diam: float = 3.125) -> None:
        self.shank_diam = shank_diam
        self._cq_object = self._make()

    def _make(self) -> cq.Workplane:
        blank = OrganiserBlank()
        organiser = blank.cq_object

        base_wp = (
            organiser
            .faces(">Z")
            .workplane(centerOption="CenterOfMass")
        )

        bit_points = (
            base_wp
            .rarray(
                self.shank_diam * 3,
                self.shank_diam * 4,
                4,
                4,
            )
            .vals()
        )
        bit_points.extend(
            base_wp
            .rarray(
                self.shank_diam * 3,
                self.shank_diam * 4,
                3,
                3,
            )
            .vals()
        )

        hole_diam = self.shank_diam + 2 * CLEARANCE.loose
        hole_depth = organiser.val().BoundingBox().zlen - 1.5 * WALL_THICK

        result = (
            base_wp
            .newObject(bit_points)
            .hole(hole_diam, depth=hole_depth)
        )
        return result


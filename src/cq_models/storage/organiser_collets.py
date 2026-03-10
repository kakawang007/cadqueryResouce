"""Organiser with holes for ER11 collets.

Migrated from cadquery-contrib/hexagonal_drawers/organiser_collets.py.
"""

from types import SimpleNamespace

import cadquery as cq

from cq_models.base import CqWorkplaneModel
from cq_models.storage.organiser_blank import OrganiserBlank


class ColletOrganiser(CqWorkplaneModel):
    """Organiser insert with shaped holes for ER11 collets.

    :param upper_diam: Upper diameter of collet (mm).
    :param cone_height: Cone height of collet (mm).
    :param lower_diam: Lower diameter of collet (mm).
    """

    def __init__(
        self,
        upper_diam: float = 11.35,
        cone_height: float = 13.55,
        lower_diam: float = 7.8,
    ) -> None:
        self.collet_dims = SimpleNamespace(
            upper_diam=upper_diam,
            cone_height=cone_height,
            lower_diam=lower_diam,
        )
        self._cq_object = self._make()

    def _make(self) -> cq.Workplane:
        dims = self.collet_dims

        collet = (
            cq.Solid.makeCone(
                dims.upper_diam / 2,
                dims.lower_diam / 2,
                dims.cone_height,
            )
            .mirror("XY")
            .translate(cq.Vector(0, 0, dims.cone_height / 3))
        )

        blank = OrganiserBlank()
        organiser = blank.cq_object

        collet_points = (
            organiser
            .faces(">Z")
            .workplane(centerOption="CenterOfMass")
            .rarray(
                dims.upper_diam * 1.5,
                dims.upper_diam * 2.3,
                3,
                2,
            )
            .vals()
        )
        collet_points.extend(
            organiser
            .faces(">Z")
            .workplane(centerOption="CenterOfMass")
            .rarray(
                dims.upper_diam * 1.5,
                dims.upper_diam * 2.3,
                2,
                1,
            )
            .vals()
        )

        collets = (
            cq.Workplane()
            .pushPoints(collet_points)
            .eachpoint(lambda loc: collet.located(loc))
        )
        return organiser.cut(collets)


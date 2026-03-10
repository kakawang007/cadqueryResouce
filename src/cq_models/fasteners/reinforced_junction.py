"""Reinforced junction using fillet.

Demonstrates reinforcing a weak junction between a box and a cylinder
by selecting the closest edge and applying a fillet.

Migrated from cadquery-contrib/Reinforce_Junction_UsingFillet.py.
"""

import cadquery as cq
from cadquery import selectors

from cq_models.base import CqWorkplaneModel


class ReinforcedJunction(CqWorkplaneModel):
    """Pipe connector with reinforced junction.

    A box base with countersunk holes and a cylindrical pipe,
    with the junction reinforced by a fillet.

    :param base_size: Width/length of the base plate (mm).
    :param base_height: Height of the base plate (mm).
    :param pipe_radius: Outer radius of the pipe (mm).
    :param pipe_height: Height of the pipe (mm).
    :param hole_diameter: Inner diameter of the pipe (mm).
    :param fillet_radius: Fillet radius for junction reinforcement (mm).
    """

    def __init__(
        self,
        base_size: float = 15.0,
        base_height: float = 2.0,
        pipe_radius: float = 4.0,
        pipe_height: float = 10.0,
        hole_diameter: float = 6.0,
        fillet_radius: float = 1.0,
    ) -> None:
        self.base_size = base_size
        self.base_height = base_height
        self.pipe_radius = pipe_radius
        self.pipe_height = pipe_height
        self.hole_diameter = hole_diameter
        self.fillet_radius = fillet_radius
        self._cq_object = self._make()

    def _make(self) -> cq.Workplane:
        # Build the base model: box + countersunk holes + cylinder + pipe hole
        model = (
            cq.Workplane("XY")
            .box(self.base_size, self.base_size, self.base_height)
            .faces(">Z")
            .rect(10.0, 10.0, forConstruction=True)
            .vertices()
            .cskHole(2.0, 4.0, 82)
            .faces(">Z")
            .circle(self.pipe_radius)
            .extrude(self.pipe_height)
            .faces(">Z")
            .hole(self.hole_diameter)
        )

        # Reinforce the junction: select closest edge from center, apply fillet
        result = (
            model
            .faces("<Z[1]")
            .edges(selectors.NearestToPointSelector((0.0, 0.0)))
            .fillet(self.fillet_radius)
        )
        return result


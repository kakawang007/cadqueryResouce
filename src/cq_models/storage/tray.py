"""Parametric storage tray with dividers and spacers.

Migrated from cadquery-contrib/tray.py.
"""

from __future__ import annotations

import cadquery as cq
from cadquery import Location as Loc, Vector as Vec
from numpy import linspace, diff

from cq_models.base import CqAssemblyModel


class Tray(CqAssemblyModel):
    """Parametric storage tray assembly with dividers and spacers.

    :param width: Tray width (mm).
    :param height: Tray height (mm - depth direction).
    :param wall: Wall / divider thickness (mm).
    :param num_dividers: Number of divider slots.
    :param wall_height: Height of walls and dividers (mm).
    """

    def __init__(
        self,
        width: float = 770,
        height: float = 460,
        wall: float = 5,
        num_dividers: int = 7,
        wall_height: float = 50,
    ) -> None:
        self.W = width
        self.H = height
        self.d = wall
        self.N = num_dividers
        self.h = wall_height
        self._name = "tray"
        self._cq_object = self._make()

    def _make_base(self) -> cq.Workplane:
        pts = linspace(-(self.W - self.d) / 2, (self.W - self.d) / 2, self.N + 2)
        return (
            cq.Workplane()
            .rect(self.W, self.H)
            .extrude(self.d)
            .pushPoints(
                [(pt, 0) for pt in pts]
                + [(0, self.H / 2 - self.d / 2), (0, -self.H / 2 + self.d / 2)]
            )
            .rect(self.d, self.d)
            .cutThruAll()
        )

    def _make_front(self) -> cq.Workplane:
        pts = linspace(-(self.W - self.d) / 2, (self.W - self.d) / 2, self.N + 2)
        return (
            cq.Workplane()
            .rect(self.W, self.d)
            .extrude(self.h - self.d)
            .faces("<Z")
            .workplane()
            .rect(self.d, self.d)
            .extrude(self.d)
            .faces("<Y")
            .workplane()
            .pushPoints([(pt, (self.h - self.d) / 2) for pt in pts])
            .rect(self.d, self.d)
            .cutThruAll()
        )

    def _make_divider(self) -> cq.Workplane:
        vpts = [
            (0, -3 * self.H / 8), (0, -self.H / 4), (0, -self.H / 8),
            (0, 0),
            (0, self.H / 8), (0, self.H / 4), (0, 3 * self.H / 8),
        ]
        return (
            cq.Workplane()
            .rect(self.d, self.H - 2 * self.d)
            .extrude(self.h - 2 * self.d)
            .faces(">Z")
            .workplane()
            .pushPoints(vpts)
            .rect(self.d, self.d)
            .cutBlind(-self.d)
            .faces("<Z")
            .workplane()
            .rect(self.d, self.d)
            .extrude(self.d)
            .pushPoints([
                (0, -self.H / 2 + self.d - self.d / 2, -(self.h - self.d) / 2),
                (0, self.H / 2 - self.d + self.d / 2, -(self.h - self.d) / 2),
            ])
            .box(self.d, self.d, self.d)
        )

    def _make_spacer(self, delta: float) -> cq.Workplane:
        return (
            cq.Workplane("XZ")
            .rect(delta - self.d, self.h - self.d)
            .pushPoints([
                (-(delta - self.d) / 2, self.h / 2 - self.d - self.d / 2),
                ((delta - self.d) / 2, self.h / 2 - self.d - self.d / 2),
            ])
            .rect(self.d, 2 * self.d)
            .extrude(self.d)
        )

    def _make(self) -> cq.Assembly:
        pts = linspace(-(self.W - self.d) / 2, (self.W - self.d) / 2, self.N + 2)
        delta = float(diff(pts)[0])

        base = self._make_base()
        divider = self._make_divider()
        front = self._make_front()

        assy = (
            cq.Assembly(base, name="base", color=cq.Color(1, 1, 0.4, 0.5))
            .add(divider, name="side_l", loc=Loc(Vec(-(self.W - self.d) / 2, 0, self.d)))
            .add(divider, name="side_r", loc=Loc(Vec((self.W - self.d) / 2, 0, self.d)))
            .add(front, name="front_f", loc=Loc(Vec(0, -(self.H - self.d) / 2, self.d)))
            .add(front, name="front_b", loc=Loc(Vec(0, (self.H - self.d) / 2, self.d)))
        )
        for i, p in enumerate(pts[1:-1]):
            assy = assy.add(self._make_divider(), name=f"div{i}", loc=Loc(Vec(p, 0, self.d)))
        for i, p in enumerate(pts[1:]):
            assy = assy.add(
                self._make_spacer(delta), name=f"spacer{i}",
                loc=Loc(Vec(p - delta / 2, self.d / 2, self.d + self.h / 2 - self.d / 2)),
            )
        return assy


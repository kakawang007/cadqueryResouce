"""Parametric door assembly with V-slot profiles.

Migrated from cadquery-contrib/door.py.
Modelling logic only - no display/preview code.
"""

from __future__ import annotations

from pathlib import Path

import cadquery as cq

from cq_models.base import CqAssemblyModel


# Default resource path for DXF profile
_DEFAULT_DXF = Path(__file__).resolve().parent.parent.parent.parent / "resources" / "vslot-2020_1.dxf"


class Door(CqAssemblyModel):
    """Parametric door frame assembly.

    :param height: Height of the door frame (mm).
    :param width: Width of the door frame (mm).
    :param slot_depth: V-slot depth for panel insertion (mm).
    :param panel_thickness: Panel thickness (mm).
    :param handle_diameter: Handle arc diameter (mm).
    :param handle_length: Handle length (mm).
    :param handle_width: Handle cross-section width (mm).
    :param dxf_profile: Path to V-slot DXF profile file.
    """

    def __init__(
        self,
        height: float = 400,
        width: float = 200,
        *,
        slot_depth: float = 6,
        panel_thickness: float = 3,
        handle_diameter: float = 20,
        handle_length: float = 50,
        handle_width: float = 4,
        dxf_profile: str | Path | None = None,
    ) -> None:
        self.height = height
        self.width = width
        self.slot_depth = slot_depth
        self.panel_thickness = panel_thickness
        self.handle_diameter = handle_diameter
        self.handle_length = handle_length
        self.handle_width = handle_width
        self._dxf_path = Path(dxf_profile) if dxf_profile else _DEFAULT_DXF
        self._name = "door"
        self._cq_object = self._make()

    def _load_profile(self) -> cq.Workplane:
        """Load V-slot profile from DXF file."""
        return cq.importers.importDXF(str(self._dxf_path)).wires()

    def _make_vslot(self, length: float) -> cq.Workplane:
        """Create a V-slot extrusion of given length."""
        profile = self._load_profile()
        return profile.toPending().extrude(length)

    def _make_connector(self) -> cq.Workplane:
        """Create a corner connector block."""
        rv = (
            cq.Workplane()
            .box(20, 20, 20)
            .faces("<X")
            .workplane()
            .cboreHole(6, 15, 18)
            .faces("<Z")
            .workplane(centerOption="CenterOfMass")
            .cboreHole(6, 15, 18)
        )
        rv.faces(">X").tag("X").end()
        rv.faces(">Z").tag("Z").end()
        return rv

    def _make_panel(self, w: float, h: float, t: float, cutout: float) -> cq.Workplane:
        """Create a door panel with handle mounting holes."""
        rv = (
            cq.Workplane("XZ")
            .rect(w, h)
            .extrude(t)
            .faces(">Y")
            .vertices()
            .rect(2 * cutout, 2 * cutout)
            .cutThruAll()
            .faces("<Y")
            .workplane()
            .pushPoints([(-w / 3, self.handle_length / 2), (-w / 3, -self.handle_length / 2)])
            .hole(3)
        )
        rv.faces(">Y").edges("%CIRCLE").edges(">Z").tag("hole1")
        rv.faces(">Y").edges("%CIRCLE").edges("<Z").tag("hole2")
        return rv

    def _make_handle(self, w: float, h: float, r: float) -> cq.Workplane:
        """Create a door handle."""
        pts = ((0, 0), (w, 0), (w, h), (0, h))
        path = cq.Workplane().polyline(pts)
        rv = (
            cq.Workplane("YZ")
            .rect(r, r)
            .sweep(path, transition="round")
            .tag("solid")
            .faces("<X")
            .workplane()
            .faces("<X", tag="solid")
            .hole(r / 1.5)
        )
        rv.faces("<X").faces(">Y").tag("mate1")
        rv.faces("<X").faces("<Y").tag("mate2")
        return rv

    def _make(self) -> cq.Assembly:
        """Assemble door frame, panel, and handle with constraints.

        :return: Solved door assembly.
        """
        H = self.height
        W = self.width
        S = self.slot_depth

        door = (
            cq.Assembly()
            .add(self._make_vslot(H), name="left")
            .add(self._make_vslot(H), name="right")
            .add(self._make_vslot(W), name="top")
            .add(self._make_vslot(W), name="bottom")
            .add(self._make_connector(), name="con_tl", color=cq.Color("black"))
            .add(self._make_connector(), name="con_tr", color=cq.Color("black"))
            .add(self._make_connector(), name="con_bl", color=cq.Color("black"))
            .add(self._make_connector(), name="con_br", color=cq.Color("black"))
            .add(
                self._make_panel(W + 2 * S, H + 2 * S, self.panel_thickness, S),
                name="panel",
                color=cq.Color(0, 0, 1, 0.2),
            )
            .add(
                self._make_handle(self.handle_diameter, self.handle_length, self.handle_width),
                name="handle",
                color=cq.Color("yellow"),
            )
        )

        # Define constraints
        (
            door
            # left profile
            .constrain("left@faces@<Z", "con_bl?Z", "Plane")
            .constrain("left@faces@<X", "con_bl?X", "Axis")
            .constrain("left@faces@>Z", "con_tl?Z", "Plane")
            .constrain("left@faces@<X", "con_tl?X", "Axis")
            # top
            .constrain("top@faces@<Z", "con_tl?X", "Plane")
            .constrain("top@faces@<Y", "con_tl@faces@>Y", "Axis")
            # bottom
            .constrain("bottom@faces@<Y", "con_bl@faces@>Y", "Axis")
            .constrain("bottom@faces@>Z", "con_bl?X", "Plane")
            # right connectors
            .constrain("top@faces@>Z", "con_tr@faces@>X", "Plane")
            .constrain("bottom@faces@<Z", "con_br@faces@>X", "Plane")
            .constrain("left@faces@>Z", "con_tr?Z", "Axis")
            .constrain("left@faces@<Z", "con_br?Z", "Axis")
            # right profile
            .constrain("right@faces@>Z", "con_tr@faces@>Z", "Plane")
            .constrain("right@faces@<X", "left@faces@<X", "Axis")
            # panel
            .constrain("left@faces@>X[-4]", "panel@faces@<X", "Plane")
            .constrain("left@faces@>Z", "panel@faces@>Z", "Axis")
            # handle
            .constrain("panel?hole1", "handle?mate1", "Plane")
            .constrain("panel?hole2", "handle?mate2", "Point")
        )

        door.solve()
        return door


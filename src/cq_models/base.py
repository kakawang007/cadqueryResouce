"""Abstract base classes for all CQ Models components.

Provides unified interfaces for CadQuery modeling classes.
All modeling modules should inherit from these base classes
to ensure consistent API across the library.

Designed to be compatible with cq-electronics' CqWorkplaneContainer
and CqAssemblyContainer interfaces.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import cadquery as cq


class CqWorkplaneModel(ABC):
    """Abstract base class for single-body CadQuery models.

    All classes that produce a ``cq.Workplane`` should inherit from this class.
    Subclasses must implement the ``_make()`` method.

    Usage::

        class MyPart(CqWorkplaneModel):
            def __init__(self, size: float = 10):
                self.size = size
                self._cq_object = self._make()

            def _make(self) -> cq.Workplane:
                return cq.Workplane("XY").box(self.size, self.size, self.size)

        part = MyPart(20)
        result = part.cq_object  # get the CadQuery Workplane
    """

    _cq_object: cq.Workplane

    @property
    def cq_object(self) -> cq.Workplane:
        """Get the CadQuery Workplane object."""
        return self._cq_object

    @abstractmethod
    def _make(self) -> cq.Workplane:
        """Create the CadQuery Workplane object. Subclasses must implement."""
        ...

    def export_step(self, path: str | Path) -> None:
        """Export the model to a STEP file.

        :param path: Output file path.
        """
        cq.exporters.export(self._cq_object, str(path), "STEP")

    def export_stl(self, path: str | Path) -> None:
        """Export the model to an STL file.

        :param path: Output file path.
        """
        cq.exporters.export(self._cq_object, str(path), "STL")


class CqAssemblyModel(ABC):
    """Abstract base class for CadQuery Assembly models.

    All classes that produce a ``cq.Assembly`` should inherit from this class.
    Subclasses must implement the ``_make()`` method.

    Usage::

        class MyAssembly(CqAssemblyModel):
            def __init__(self):
                self._name = "my_assembly"
                self._cq_object = self._make()

            def _make(self) -> cq.Assembly:
                return cq.Assembly()

        assy = MyAssembly()
        result = assy.cq_object  # get the CadQuery Assembly
    """

    _cq_object: cq.Assembly
    _name: str = "assembly"

    @property
    def cq_object(self) -> cq.Assembly:
        """Get the CadQuery Assembly object."""
        return self._cq_object

    @property
    def name(self) -> str:
        """Assembly name."""
        return self._name

    def cq_part(self, name: str) -> cq.Shape | cq.Workplane:
        """Get a part from the CadQuery assembly by name.

        :param name: Part name in the assembly.
        :raises Exception: If the name is not found.
        """
        result = self._cq_object.objects[name].obj
        if result is None:
            raise Exception(f"Invalid name: '{name}'.")
        return result

    def sub_assembly_name(self, name: str) -> str:
        """Generate a sub-assembly name with the parent prefix.

        :param name: Sub-assembly local name.
        """
        return f"{self._name}__{name}"

    @abstractmethod
    def _make(self) -> cq.Assembly:
        """Create the CadQuery Assembly object. Subclasses must implement."""
        ...

    def export_step(self, path: str | Path) -> None:
        """Export the assembly to a STEP file.

        :param path: Output file path.
        """
        self._cq_object.save(str(path))


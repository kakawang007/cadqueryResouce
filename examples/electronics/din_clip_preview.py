"""Example usage of CadQuery Electronics DIN clip."""

from cq_models.electronics.mechanical.din_clip import DinClip

din_clip = DinClip()
result = din_clip.cq_object

from ocp_vscode import show

show(result, names=["din_clip"])  # type: ignore[name-defined] # noqa: F821

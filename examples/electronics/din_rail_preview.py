"""Example usage of CadQuery Electronics top hat DIN rail."""

from cq_models.electronics.mechanical.din_rail import TopHat
from ocp_vscode import show

top_hat = TopHat(100, slots=True)
result = top_hat.cq_object

# if "show_object" in locals():
    # show_object(result, name="din_rail")  # type: ignore[name-defined] # noqa: F821
show(result, names=["din_rail"])  # type: ignore[name-defined] # noqa: F821

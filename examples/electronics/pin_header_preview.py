"""Example usage of CadQuery Electronics pin header."""

from cq_models.electronics.connectors.headers import PinHeader
from ocp_vscode import show

pin_header = PinHeader(rows=2, columns=10, simple=False)
result = pin_header.cq_object

# if "show_object" in locals():
#     show_object(result, name="pin_header")  # type: ignore[name-defined] # noqa: F821
show(result, names=["pin_header"])  # type: ignore[name-defined] # noqa: F821

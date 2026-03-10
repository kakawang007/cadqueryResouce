"""RJ45 jack preview.

Usage:
    conda activate cq-user
    cd D:\\dev\\sg\\cadqueryResouce
    python examples/electronics/rj45_preview.py
"""

from cq_models.electronics.connectors.rj45 import JackSurfaceMount
from ocp_vscode import show

jack = JackSurfaceMount(simple=False)
show(jack.cq_object, name="rj45_jack")


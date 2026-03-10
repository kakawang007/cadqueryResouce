"""BGA package preview.

Usage:
    conda activate cq-user
    cd D:\\dev\\sg\\cadqueryResouce
    python examples/electronics/bga_preview.py
"""

from cq_models.electronics.smd.bga import BGA
from ocp_vscode import show

bga = BGA(20, 20, simple=False)
show(bga.cq_object, names=["bga_package"])


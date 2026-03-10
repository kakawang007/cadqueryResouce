"""Reinforced junction preview.

Usage:
    conda activate cq-user
    cd D:\\dev\\sg\\cadqueryResouce
    python examples/reinforced_junction_preview.py
"""

from cq_models.fasteners.reinforced_junction import ReinforcedJunction
from ocp_vscode import show

junction = ReinforcedJunction()
show(junction.cq_object, name="reinforced_junction")


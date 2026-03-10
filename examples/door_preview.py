"""Door assembly preview.

Usage:
    conda activate cq-user
    cd D:\\dev\\sg\\cadqueryResouce
    python examples/door_preview.py
"""

from cq_models.furniture.door import Door
from ocp_vscode import show

door = Door(height=400, width=200)
show(door.cq_object, name="door")


"""Hexagonal drawers preview - frame, drawer, and organisers.

Usage:
    conda activate cq-user
    cd D:\\dev\\sg\\cadqueryResouce
    python examples/hexagonal_drawers_preview.py
"""

from cq_models.storage.hexagonal_frame import HexagonalFrame
from cq_models.storage.hexagonal_drawer import HexagonalDrawer
from cq_models.storage.organiser_collets import ColletOrganiser
from cq_models.storage.organiser_bits import BitOrganiser
from ocp_vscode import show

frame = HexagonalFrame()
drawer = HexagonalDrawer()
collet_org = ColletOrganiser()
bit_org = BitOrganiser()

show(
    frame.cq_object,
    drawer.cq_object,
    collet_org.cq_object,
    bit_org.cq_object,
    names=["frame", "drawer", "collet_organiser", "bit_organiser"],
)


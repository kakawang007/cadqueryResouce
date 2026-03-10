"""Storage tray preview.

Usage:
    conda activate cq-user
    cd D:\\dev\\sg\\cadqueryResouce
    python examples/tray_preview.py
"""

from cq_models.storage.tray import Tray
from ocp_vscode import show

tray = Tray(width=770, height=460, num_dividers=7)
show(tray.cq_object, names=["tray"])


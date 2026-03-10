"""Raspberry Pi 3 Model B preview.

Usage:
    conda activate cq-user
    cd D:\\dev\\sg\\cadqueryResouce
    python examples/electronics/raspberry_pi_preview.py
"""

from cq_models.electronics.rpi.rpi3b import RPi3b
from ocp_vscode import show

rpi = RPi3b(simple=False)
show(rpi.cq_object, names=["raspberry_pi_3b"])


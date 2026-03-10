import cadquery as cq
from ocp_vscode import show as show_object

 # Parameters
H = 400
W = 200
D = 350

PROFILE = cq.importers.importDXF("vslot-2020_1.dxf").wires()

show_object(PROFILE)
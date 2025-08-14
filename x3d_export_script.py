import os
from paraview.simple import *

active_objects = GetActiveSource()
renderView1 = GetActiveViewOrCreate('RenderView')

all_sources = GetSources()

for source in all_sources.values():
    if source != active_objects:
        Hide(source, renderView1)
    else:
        Show(source, renderView1)

renderView1.Update()

name = active_objects.GetXMLLabel().replace(" ", "_")

export_dir = r'C:\Users\Blue9\OneDrive\Pictures\Documents\ParaView_Projects\exported_projects\c1'
output_path = os.path.join(export_dir, f"{name}.x3d")

i = 1
while os.path.exists(output_path):
    output_path = os.path.join (export_dir, f"{name} ({i}).x3d")
    i += 1

ExportView(output_path, view=renderView1, ExportColorLegends=1)

print(f'Exported view with active source: {name} to {output_path}')

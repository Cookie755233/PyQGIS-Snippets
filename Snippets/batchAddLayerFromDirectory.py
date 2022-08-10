'''
### MAP ALL LAYERS WITHIN DIRECTORY HIERARCHICALLY ###

Add all desired data type(i.e., *.shp, *.gpkg, etc.) within folder to the working canvas,
while keeping the correct data hierarchy.
'''


import glob
import os
import re

PATH = "/Users/name/path_to_root_folder"
ROOT = QgsProject.instance().layerTreeRoot()
CRS = 3826
ENCODING = 'utf-8'


def add_layer(item_path, parent):
    if item_path.endswith('shp') or item_path.endswith('kml') or item_path.endswith('gpkg'): # You can modify this to your desired format only
        # Load Layer
        layer_name = re.search(r'(.*)\.[a-zA-Z]+',  # remove the format type 
                               os.path.basename(item_path)).group(1)

        layer = QgsVectorLayer(item_path, layer_name, 'ogr')

        # Set CRS
        crs = layer.crs()
        crs.createFromId(CRS)
        layer.setCrs(crs)

        # Set Encoding
        layer.setProviderEncoding(ENCODING)

        # Create layer, set False to prevent duplicates
        QgsProject.instance().addMapLayer(layer, False)

        # Put it within parent group
        parent.addLayer(layer)


def recur(path, root):
    if os.path.isdir(path):
        # Create group
        parent_name = os.path.basename(path)
        parent = root.addGroup(parent_name)
        
        item_paths_within = glob.glob(f'{path}/*')
        for item in item_paths_within:
            # if isdir() -> recursively search for deeper folder
            if os.path.isdir(item): 
                recur(item, parent)
            
            # if isfile() -> add layers within folder
            elif os.path.isfile(item):
                add_layer(item, parent)


recur(PATH, ROOT)

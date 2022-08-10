'''
### SPLIT LAYER BY FIELD VALUES ###

Split a layer into multiple layers by attribute by iterate through each value, 
and split by `qgis:extractbyexpression` functions.

i.e.,
                     outputGroupName ______________________
targetLayerName       | layer:001          layer:003      |
  | cls | name |      | | cls | name |     | cls | name | |
  | --- | ---- |      | | --- | ---- |     | --- | ---- | |
  | 001 | AAAA |      | | 001 | AAAA |     | 003 | DDDD | |
  | 002 | BBBB |      |                    | 003 | EEEE | |
  | 002 | CCCC |   -> |                    | 003 | FFFF | |
  | 003 | DDDD |      | layer:002          | 003 | GGGG | |
  | 003 | EEEE |      | | cls | name |                    |
  | 003 | FFFF |      | | 002 | BBBB |                    |
  | 003 | GGGG |      | | 002 | CCCC |                    |
                      |___________________________________|
  '''

# Change variables to valid names in your local machine
TARGET_LAYER = 'targetLayerName' 
GROUP_NAME = 'groupName'  # Container group's name
FIELD_NAME = 'attrName'   # name of the field you're splitting

layer = QgsProject.instance().mapLayersByName(TARGET_LAYER)[0]      # Select the target layer
group = QgsProject.instance().layerTreeRoot().addGroup(GROUP_NAME)  # Create a container group for outputs

unique_values_of_field = layer.uniqueValues( layer.fields().indexOf('FIELD_NAME') )

for val in unique_values_of_field:
    expression = f'{FIELD_NAME} = {val}'                     # Have as many expression as you want
    
    selected = processing.run(
    "qgis:extractbyexpression", {
        'INPUT': layer, 
        'EXPRESSION': expression,
        'OUTPUT':'TEMPORARY_OUTPUT'
        }
    )['OUTPUT']
    
    if selected.featureCount():                              # Check if output returns QgsVectorLayer
        selected.setName(str(val))                           # You can change this to desired layer name
        QgsProject.instance().addMapLayer(selected,False)    # Add map to panel without showing it
        group.addLayer(selected)                             # move layer under group

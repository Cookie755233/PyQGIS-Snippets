'''
### QUERY DATA & OUTPUT AS TEMPORARY LAYER ###

Only suggest using this only if you have multiple layers with the same query, 
or having to do this in the middle of other tasks.
'''

# Import modules
import processing

# Change with your need
name = 'layerName'
expression = ''' 
            "field1" > 10_000 and 
            "field2" != 'something' and 
            "field3" in ('A', 'B', 'C', 'D') and 
            "field4" = 'hello world' 
            '''

# Select the layer
lyr = QgsProject.instance().mapLayersByName(name)[0]

# Run the algorithm -> selected: QgsVectorLayer
selected = processing.run(
    "qgis:extractbyexpression", {
        'INPUT'     : lyr,
        'EXPRESSION': expression,
        'OUTPUT'    : 'TEMPORARY_OUTPUT'
    }
)['OUTPUT']

# Add layer to the panel
QgsProject.instance().addMapLayer(selected)

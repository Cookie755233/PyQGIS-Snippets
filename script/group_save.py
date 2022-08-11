from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProject,
                       QgsProcessing,
                       QgsProcessingParameterFile,
                       QgsProcessingAlgorithm,
                       QgsProcessingException,
                       QgsProcessingOutputNumber,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterVectorDestination,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterEnum,
                       QgsLayerTreeGroup,
                       QgsVectorFileWriter)
from qgis import processing
import os


def tr(string):
    return QCoreApplication.translate('Processing', string)
    
def get_group(layer: int, 
              parent: QgsLayerTreeGroup, 
              groups=[]):
    if layer:
        groups.append(parent.name())
    for child in parent.children():
        if isinstance(child, QgsLayerTreeGroup):
            get_group(layer+1, child)
            
    return groups
    
GROUP = get_group(0, QgsProject.instance().layerTreeRoot())

class ExampleProcessingAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer,
    creates some new layers and returns some results.
    """
    
    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        # Must return a new copy of your algorithm.
        return ExampleProcessingAlgorithm()

    def name(self):
        """
        Returns the unique algorithm name.
        """
        return 'bufferrasterextend'

    def displayName(self):
        """
        Returns the translated algorithm name.
        """
        return self.tr('Group save')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to.
        """
        return self.tr('Example scripts')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs
        to.
        """
        return 'examplescripts'

    def shortHelpString(self):
        """
        Returns a localised short help string for the algorithm.
        """
        return self.tr('Save all layers within group')

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and outputs of the algorithm.
        """
        # 'INPUT' is the recommended name for the main input
        # parameter.
        self.addParameter(
            QgsProcessingParameterEnum(
                'INPUT',
                tr('Groups in your current working space'),
                options=[tr(i) for i in GROUP],
                defaultValue=0,
                optional=False
                )
            )
        self.addParameter(
            QgsProcessingParameterFile(
                'OUTPUT_DIR',
                self.tr("Output directory"),
                behavior=QgsProcessingParameterFile.Folder
                )
            )
        # 'OUTPUT' is the recommended name for the main output
        # parameter.
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                'OUTPUT',
                self.tr('Output')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        source_folder_path = self.parameterAsFile(parameters, 
                                                  'OUTPUT_DIR', 
                                                  context)
        
        name_index = self.parameterAsEnum(parameters,
                                          'INPUT',
                                          context)
        group = QgsProject.instance().layerTreeRoot().findGroup(GROUP[name_index])
        result = {}
        for child in group.children():
            lyr = child.layer()
            result[lyr.name()] = f"{source_folder_path}\\{lyr.name()}.kml"
            QgsVectorFileWriter.writeAsVectorFormat(layer=lyr, 
                                                    fileName=f"{source_folder_path}//{lyr.name()}.kml", 
                                                    fileEncoding="utf-8", 
                                                    destCRS=lyr.crs(), 
                                                    driverName="KML")
        
        return result
        

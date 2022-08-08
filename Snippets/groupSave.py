'''
### SAVE ALL LAYERS WITHIN GROUP TO A FOLDER ###

writeAsVectorFormat(
    layer: QgsVectorLayer, 
    fileName: str, 
    fileEncoding: str, 
    destCRS: QgsCoordinateReferenceSystem = QgsCoordinateReferenceSystem(),
    driverName: str = '',
    onlySelected: bool = False,
    datasourceOptions: Iterable[str] = [],
    layerOptions: Iterable[str] = [],
    skipAttributeCreation: bool = False,
    newFilename: str = '', 
    symbologyExport: QgsVectorFileWriter.SymbologyExport = QgsVectorFileWriter.NoSymbology,
    symbologyScale: float = 1,
    filterExtent: QgsRectangle = None,
    overrideGeometryType: QgsWkbTypes.Type = QgsWkbTypes.Unknown,
    forceMulti: bool = False,
    includeZ: bool = False,
    attributes: Iterable[int] = [],
    fieldValueConverter: QgsVectorFileWriter.FieldValueConverter = None
    ) → Tuple[QgsVectorFileWriter.WriterError, str]

Docuemntation has claimed "Deprecated since version QGIS: 3.20 use writeAsVectorFormatV3 instead", yet it's most likely doable.
'''
# Select your own group name here
groupName = "groupName" 

# Find the group in your working panel
root = QgsProject.instance().layerTreeRoot()
group = root.findGroup(groupName)

# Define output directory (MAKE SURE DIR EXISTS!)
output_dir = '/Users/userName/Desktop/'

# Iterate through the group and save them to your desired format
for child in group.children():
    layer = child.layer()
    QgsVectorFileWriter.writeAsVectorFormat(
        layer, output_dir+layer.name(), "utf-8", layer.crs(), "KML")

    # to .shp
    # QgsVectorFileWriter.writeAsVectorFormat(
    #	layer, output_dir+layer.name, "utf-8", layer.crs(), "ESRI Shapfile")

    # to .gpkg
    # QgsVectorFileWriter.writeAsVectorFormat(
    #   layer, output_dir+layer.name, "utf-8", layer.crs(), "GPKG")

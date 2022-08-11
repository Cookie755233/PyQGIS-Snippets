def adjust_symbology(rlayer, 
                     colorDict= {'5':'#d7191c',
                                 '4':'#fdae61',
                                 '3':'#ffffbf',
                                 '2':'#abdda4',
                                 '1':'#2b83ba'}
                     ) -> None:
    '''  
    INPUT:
        rlayer : QgsRasterLayer
        colorDict: dict 

    ------------------------------------
    OUTPUT:
        create canvas components -> None 
    '''
    extent = rlayer.extent()                                        # define extent
    provider = rlayer.dataProvider()                                # create dataProvider
    myColorRamp = QgsColorRampShader()                              # create QgscolorRampShader
    myColorRamp.setColorRampType(QgsColorRampShader.Interpolated)   # set colorramp type to 'interpolated' (alternatives: QgsColorRampShader.Discrete)
    
    # <-- make band stastistics -->
    stats = provider.bandStatistics(1, QgsRasterBandStats.All, extent, 0)
    min_ = Decimal(stats.minimumValue)      # IMPORTANT: import `Decimal` module to prevent floating point issue
    max_ = Decimal(stats.maximumValue)      # IMPORTANT: import `Decimal` module to prevent floating point issue
    etape = (min_ + max_) / 5
    interval_orange = min_ + (etape*1)
    interval_jaune = min_ + (etape*2)
    interval_vert = min_ + (etape*3)
    
    # <-- create colorRampList -->
    colorRampList = [
        QgsColorRampShader.ColorRampItem(min_, QColor(colorDict['1']), str(min_)),
        QgsColorRampShader.ColorRampItem(interval_orange, QColor(colorDict['2']), str(interval_orange)),
        QgsColorRampShader.ColorRampItem(interval_jaune, QColor(colorDict['3']), str(interval_jaune)),
        QgsColorRampShader.ColorRampItem(interval_vert, QColor(colorDict['4']), str(interval_vert)),
        QgsColorRampShader.ColorRampItem(max_, QColor(colorDict['5']), str(max_))
        ]
    myColorRamp.setColorRampItemList(colorRampList)
    
    # <-- create raster Shader -->
    myRasterShader = QgsRasterShader()
    myRasterShader.setRasterShaderFunction(myColorRamp)
    myPseudoRenderer = QgsSingleBandPseudoColorRenderer(rlayer.dataProvider(), 
                                                        1,
                                                        myRasterShader) # qgis.core.QgsSingleBandPseudoColorRenderer(input: QgsRasterInterface, band: int = -1, shader: QgsRasterShader = None)
    rlayer.setRenderer(myPseudoRenderer)
    rlayer.setOpacity(0.8)   # OPTIONAL
    rlayer.triggerRepaint()
    
    # <-- refresh to apply the above -->
    iface.layerTreeView().refreshLayerSymbology(rlayer.id())

    


def png_save(rlayer, extent, outfile_path) -> None:
    '''
    ### SAVE EXTENT TO PNG ###
    INPUT:
        rlayer : QgsRasterLayer
        extent : QgsRectangle
        outfile_path: str
            # should be a full path but without filetype suffix, i.e., '/Users/user/your_location/outfile_name
                       
    ------------------------------------
    OUTPUT:
        Save desired extent to image. -> None 
    '''
    bg_color = QColor(255, 255, 255, 255) # white bg

    # <-- create image -->
    img = QImage(QSize(800, 800), QImage.Format_ARGB32_Premultiplied)
    img.fill(bg_color.rgba())

    # <-- create painter -->
    painter = QPainter()
    painter.begin(img)
    painter.setRenderHint(QPainter.Antialiasing)

    # <-- create map settings -->
    mapSettings = QgsMapSettings()
    mapSettings.setBackgroundColor(bg_color)

    # <-- set layers to render -->
    mapSettings.setLayers([rlayer])

    # <- set extent -->
    rect = QgsRectangle(extent)
    rect.scale(1)
    mapSettings.setExtent(rect)

    # <-- set ouptut size -->
    mapSettings.setOutputSize(img.size())

    # <-- setup qgis map renderer -->
    render = QgsMapRendererCustomPainterJob(mapSettings, painter)
    render.start()
    render.waitForFinished()

    # <-- close painter -->
    painter.end()

    # <-- save -->
    img.save(f'{outfile_path}.png')



''' USAGE (uncomment the code to try with your local machine)

TASK: 
  Given 100 .TIF files, and convert them to png.


CODE: 
def do_task(tif_folder_path, outfile_path):
    tifs = glob.glob(f"{TIF}*.tif")
    
    for tif in tifs:
        outfile_name = os.path.basename(tif)
        rlayer = QgsRasterLayer(tif, outfile_name)
        adjust_symbology(rlayer)
        png_save(rlayer, 
                 rlayer.extent(), 
                 os.path.join(outfile_path, outfile_name))
'''

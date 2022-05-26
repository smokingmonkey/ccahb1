###########################################################################################
                                       # Librerías #
###########################################################################################

from osgeo import gdal

import warnings
import os
import glob

warnings.filterwarnings('ignore')

###########################################################################################
                                       # Algoritmo #
###########################################################################################

def transformacion_datos_raster():
    archivo_raster = max(glob.glob(os.path.join(os.getcwd(),'datos\\archivos\\raster_original')+'\\*'), key=os.path.getctime)
    raster_original = gdal.Open(archivo_raster)
    arreglo_raster = raster_original.GetRasterBand(1).ReadAsArray()
    raster_convertido = gdal.Warp(os.path.join(os.getcwd(),'datos\\archivos\\raster_transformado')+'\\'+'transformado_'+os.path.basename(archivo_raster)
                                 ,raster_original
                                 ,dstSRS='EPSG:4326')
    return raster_convertido

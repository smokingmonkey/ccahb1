from osgeo import gdal

import warnings
import os
import glob

warnings.filterwarnings('ignore')

class transformacion_raster_original:
    def __init__(self,ruta_raster_original,ruta_raster_transformado):
        self.ruta_raster_original=ruta_raster_original
        self.ruta_raster_transformado=ruta_raster_transformado

    def apertura_raster_original(self):
        self.archivo_raster = max(glob.glob(os.path.join(os.getcwd(), self.ruta_raster_original) + '\\*'),
                             key=os.path.getctime)
        self.raster_original = gdal.Open(self.archivo_raster)
        self.arreglo_raster = self.raster_original.GetRasterBand(1).ReadAsArray()

    def transformacion_datos_raster(self):
        self.raster_transformado=gdal.Warp(os.path.join(os.getcwd(),
                                      self.ruta_raster_transformado) + '\\' + 'transformado_' + os.path.basename(self.archivo_raster)
                                     ,self.raster_original
                                     ,dstSRS='EPSG:4326')

    def ver_raster_transformado(self):
        return self.raster_transformado

t1=transformacion_raster_original('datos\\archivos\\raster_original','datos\\archivos\\raster_transformado')
print(t1.apertura_raster_original())
###########################################################################################
                                       # Librerías #
###########################################################################################
import asf_search as asf

import getpass
import zipfile
import os
import warnings
import glob

warnings.filterwarnings('ignore')

###########################################################################################
                                # Lectura de rutas de archivos #
###########################################################################################

archivo_rutas='rutas_archivos.txt'

with open(archivo_rutas,'r', encoding="utf-8") as archivo:
    rutas = [line.rstrip('\n') for line in archivo]

ruta_zip_raster=rutas[0]
ruta_archivos_raster=rutas[1]

###########################################################################################
                                       # Algoritmo #
###########################################################################################

usuario = input ('Usuario: ')
contraseña = getpass.getpass('Contraseña:')
sesion_principal = asf.ASFSession()
sesion_principal.auth_with_creds(usuario,contraseña)

geolocalizacion = 'POLYGON((-75.4 6.12,-75.4 6.02,-75.25 6.02,-75.25 6.12,-75.4 6.12))'
resultados_geolocalizacion = asf.geo_search(platform='ALOS'
                                           ,processingLevel='RTC_HI_RES'
                                           ,intersectsWith=geolocalizacion
                                           ,maxResults=1)

resultados_geolocalizacion.download(path=ruta_zip_raster, session=sesion_principal)

zips_raster = [zraster for zraster in glob.glob(ruta_zip_raster+"\\*.zip")]
nombre_zip_raster = max(zips_raster, key=os.path.getctime)

with zipfile.ZipFile(nombre_zip_raster, 'r') as referencia_zip:
    referencia_zip.extractall(ruta_archivos_raster)
###########################################################################################
                                       # Librerías #
###########################################################################################

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import procesamiento_raster as proceso_raster

import warnings
import os
import delimitacion_cuenca

warnings.filterwarnings('ignore')
sns.set_palette('husl')

###########################################################################################
                            # Lectura de rutas de archivos #
###########################################################################################

ruta_archivos_resultados_graficas=os.path.join(os.getcwd(),'datos\\archivos\\resultados\\graficas')
mapa_coordenado=proceso_raster.mapa_coordenado

###########################################################################################
                                       # Algoritmo #
###########################################################################################

def procesamiento_red_drenaje(malla_direccion_flujo,malla_acumulacion_flujo,raster_elevacion_limitado_maximo,raster_elevacion_limitado_seleccionado):
    malla_red_drenaje_altos_maximo = raster_elevacion_limitado_maximo.extract_river_network(malla_direccion_flujo,malla_acumulacion_flujo>=np.percentile(malla_acumulacion_flujo,99.9))
    malla_red_drenaje_medios_maximo = raster_elevacion_limitado_maximo.extract_river_network(malla_direccion_flujo,malla_acumulacion_flujo>=np.percentile(malla_acumulacion_flujo,99.5))
    malla_red_drenaje_bajos_maximo = raster_elevacion_limitado_maximo.extract_river_network(malla_direccion_flujo,malla_acumulacion_flujo>=np.percentile(malla_acumulacion_flujo,99))

    malla_red_drenaje_altos_seleccionado = raster_elevacion_limitado_seleccionado.extract_river_network(malla_direccion_flujo,malla_acumulacion_flujo>=np.percentile(malla_acumulacion_flujo,99.9))
    malla_red_drenaje_medios_seleccionado = raster_elevacion_limitado_seleccionado.extract_river_network(malla_direccion_flujo,malla_acumulacion_flujo>=np.percentile(malla_acumulacion_flujo,99.5))
    malla_red_drenaje_bajos_seleccionado = raster_elevacion_limitado_seleccionado.extract_river_network(malla_direccion_flujo,malla_acumulacion_flujo>=np.percentile(malla_acumulacion_flujo,99))

    fig6, axis6 = plt.subplots(1, 3, figsize=(14, 6))
    fig6.patch.set_alpha(0)

    for arroyo in malla_red_drenaje_altos_maximo['features']:
        delimitacion = np.asarray(arroyo['geometry']['coordinates'])
        axis6[0].plot(delimitacion[:, 0], delimitacion[:, 1])

    axis6[0].set_title('Red de drenajes altos', fontsize=14, fontweight='bold')
    axis6[0].set_xlabel('Longitud')
    axis6[0].set_ylabel('Latitud')
    axis6[0].grid()

    for arroyo in malla_red_drenaje_medios_maximo['features']:
        delimitacion = np.asarray(arroyo['geometry']['coordinates'])
        axis6[1].plot(delimitacion[:, 0], delimitacion[:, 1])

    axis6[1].set_title('Red de drenajes medios', fontsize=14, fontweight='bold')
    axis6[1].set_xlabel('Longitud')
    axis6[1].set_ylabel('Latitud')
    axis6[1].grid()

    for arroyo in malla_red_drenaje_bajos_maximo['features']:
        delimitacion = np.asarray(arroyo['geometry']['coordinates'])
        axis6[2].plot(delimitacion[:, 0], delimitacion[:, 1])

    axis6[2].set_title('Red de drenajes bajos', fontsize=14, fontweight='bold')
    axis6[2].set_xlabel('Longitud')
    axis6[2].set_ylabel('Latitud')
    axis6[2].grid()

    fig6.tight_layout()
    fig6.savefig(ruta_archivos_resultados_graficas+'\\'+'MapaDrenajeCuencaMaxima.png', bbox_inches = "tight")

    fig7, axis7 = plt.subplots(1, 3, figsize=(20, 6))
    fig7.patch.set_alpha(0)

    for arroyo in malla_red_drenaje_altos_seleccionado['features']:
        delimitacion = np.asarray(arroyo['geometry']['coordinates'])
        axis7[0].plot(delimitacion[:, 0], delimitacion[:, 1])

    axis7[0].set_title('Red de drenajes altos', fontsize=14, fontweight='bold')
    axis7[0].set_xlabel('Longitud')
    axis7[0].set_ylabel('Latitud')
    axis7[0].grid()

    for arroyo in malla_red_drenaje_medios_seleccionado['features']:
        delimitacion = np.asarray(arroyo['geometry']['coordinates'])
        axis7[1].plot(delimitacion[:, 0], delimitacion[:, 1])

    axis7[1].set_title('Red de drenajes medios', fontsize=14, fontweight='bold')
    axis7[1].set_xlabel('Longitud')
    axis7[1].set_ylabel('Latitud')
    axis7[1].grid()

    for arroyo in malla_red_drenaje_bajos_seleccionado['features']:
        delimitacion = np.asarray(arroyo['geometry']['coordinates'])
        axis7[2].plot(delimitacion[:, 0], delimitacion[:, 1])

    axis7[2].set_title('Red de drenajes bajos', fontsize=14, fontweight='bold')
    axis7[2].set_xlabel('Longitud')
    axis7[2].set_ylabel('Latitud')
    axis7[2].grid()

    fig7.tight_layout()
    fig7.savefig(ruta_archivos_resultados_graficas+'\\'+'MapaDrenajeCuencaSeleccionada.png', bbox_inches = "tight")

def procesamiento_red_inundacion(malla_punto_drenaje_alto,raster_elevacion_limitado_maximo,raster_elevacion_limitado_seleccionado):
    vista_malla_delimitacion_alto_drenaje_maximo=raster_elevacion_limitado_maximo.view(malla_punto_drenaje_alto, nodata=np.nan)
    vista_extension_inundacion_maximo=raster_elevacion_limitado_maximo.view(malla_punto_drenaje_alto<3,nodata=np.nan)

    vista_malla_delimitacion_alto_drenaje_seleccionado=raster_elevacion_limitado_seleccionado.view(malla_punto_drenaje_alto, nodata=np.nan)
    vista_extension_inundacion_seleccionado=raster_elevacion_limitado_seleccionado.view(malla_punto_drenaje_alto<3,nodata=np.nan)

    fig8,axis8 = plt.subplots(1,2,figsize=(12,6))
    fig8.patch.set_alpha(0)


    img811=axis8[0].imshow(vista_malla_delimitacion_alto_drenaje_maximo
                          ,extent=raster_elevacion_limitado_maximo.extent
                          ,cmap='terrain')
    fig8.colorbar(img811
                 ,ax=axis8[0]
                 ,label='Distancia al punto de drenaje más cercano')
    axis8[0].set_title('Acumulación respecto a puntos de drenaje'
                      ,fontsize=14
                      ,fontweight='bold')
    axis8[0].set_xlabel('Longitud')
    axis8[0].set_ylabel('Latitud')
    axis8[0].grid()

    img812=axis8[1].imshow(vista_extension_inundacion_maximo
                          ,extent=raster_elevacion_limitado_maximo.extent
                          ,cmap='Blues'
                          ,zorder=1)
    fig8.colorbar(img812
                 ,ax=axis8[1]
                 ,label='Profundidad relativa')
    axis8[1].set_title('Mapa de inundación'
                      ,fontsize=14
                      ,fontweight='bold')
    axis8[1].set_xlabel('Longitud')
    axis8[1].set_ylabel('Latitud')
    axis8[1].grid()

    fig8.tight_layout()
    fig8.savefig(ruta_archivos_resultados_graficas+'\\'+'MapaInundacionCuencaMaxima.png', bbox_inches = "tight")

    fig9,axis9 = plt.subplots(1,2,figsize=(20,6))
    fig9.patch.set_alpha(0)


    img911=axis9[0].imshow(vista_malla_delimitacion_alto_drenaje_seleccionado
                         ,extent=raster_elevacion_limitado_seleccionado.extent
                         ,cmap='terrain')
    fig9.colorbar(img911
                 ,ax=axis9[0]
                 ,label='Distancia al punto de drenaje más cercano')
    axis9[0].set_title('Acumulación respecto a puntos de drenaje'
                      ,fontsize=14
                      ,fontweight='bold')
    axis9[0].set_xlabel('Longitud')
    axis9[0].set_ylabel('Latitud')
    axis9[0].grid()

    img912=axis9[1].imshow(vista_extension_inundacion_seleccionado
                          ,extent=raster_elevacion_limitado_seleccionado.extent
                          ,cmap='Blues'
                          ,zorder=1)
    fig9.colorbar(img912
                 ,ax=axis9[1]
                 ,label='Profundidad relativa')
    axis9[1].set_title('Mapa de inundación'
                      ,fontsize=14
                      ,fontweight='bold')
    axis9[1].set_xlabel('Longitud')
    axis9[1].set_ylabel('Latitud')
    axis9[1].grid()

    fig9.tight_layout()
    fig9.savefig(ruta_archivos_resultados_graficas+'\\'+'MapaInundacionCuencaSeleccionada.png', bbox_inches = "tight")
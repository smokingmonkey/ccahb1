###########################################################################################
                                       # Librerías #
###########################################################################################

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import warnings
import copy
import os
import procesamiento_raster

warnings.filterwarnings('ignore')
sns.set_palette('husl')

###########################################################################################
                                 # Parámetros generales #
###########################################################################################

mapa_coordenado= procesamiento_raster.mapa_coordenado
ruta_archivos_resultados_graficas=os.path.join(os.getcwd(),'datos\\archivos\\resultados\\graficas')
ruta_archivos_resultados_rasters=os.path.join(os.getcwd(),'datos\\archivos\\resultados\\rasters')

###########################################################################################
                                       # Algoritmo #
###########################################################################################

def limites_cuenca(raster_elevacion,malla_direccion_flujo,malla_acumulacion_flujo,longitud_flujo_seleccionada,latitud_flujo_seleccionada):
    maximo_punto_flujo=np.where(malla_acumulacion_flujo==malla_acumulacion_flujo.max())
    columna_flujo_maximo=maximo_punto_flujo[1][0]
    fila_flujo_maximo=maximo_punto_flujo[0][0]

    longitud_acumulacion_cercana=raster_elevacion.snap_to_mask(malla_acumulacion_flujo>=np.percentile(malla_acumulacion_flujo,99.5),(longitud_flujo_seleccionada, latitud_flujo_seleccionada))[0]
    latitud_acumulacion_cercana=raster_elevacion.snap_to_mask(malla_acumulacion_flujo>=np.percentile(malla_acumulacion_flujo,99.5),(longitud_flujo_seleccionada, latitud_flujo_seleccionada))[1]

    malla_delimitacion_direccion_flujo_maxima=raster_elevacion.catchment(fdir=malla_direccion_flujo
                                                                        ,x=columna_flujo_maximo
                                                                        ,y=fila_flujo_maximo
                                                                        ,dirmap=mapa_coordenado
                                                                        ,nodata=0.0
                                                                        ,xytype='index')

    malla_delimitacion_direccion_flujo_seleccionado=raster_elevacion.catchment(fdir=malla_direccion_flujo
                                                                              ,x=longitud_acumulacion_cercana
                                                                              ,y=latitud_acumulacion_cercana
                                                                              ,dirmap=mapa_coordenado
                                                                              ,nodata=0.0
                                                                              ,xytype='coordinate')

    return malla_delimitacion_direccion_flujo_maxima,malla_delimitacion_direccion_flujo_seleccionado

def procesamiento_cuenca(raster_elevacion,malla_elevacion_planicies_corregida,malla_direccion_flujo,malla_acumulacion_flujo,malla_delimitacion_direccion_flujo_maxima,malla_delimitacion_direccion_flujo_seleccionado):
    raster_elevacion_limitado_maximo=copy.deepcopy(raster_elevacion)
    raster_elevacion_limitado_seleccionado=copy.deepcopy(raster_elevacion)

    raster_elevacion_limitado_maximo.clip_to(malla_delimitacion_direccion_flujo_maxima)
    vista_malla_delimitacion_flujo_maximo = raster_elevacion_limitado_maximo.view(malla_elevacion_planicies_corregida,nodata=np.nan)
    vista_malla_delimitacion_direccion_flujo_maximo = raster_elevacion_limitado_maximo.view(malla_direccion_flujo,nodata=np.nan)
    vista_malla_delimitacion_acumulacion_flujo_maximo = raster_elevacion_limitado_maximo.view(malla_acumulacion_flujo,nodata=np.nan)

    raster_elevacion_limitado_seleccionado.clip_to(malla_delimitacion_direccion_flujo_seleccionado)
    vista_malla_delimitacion_flujo_seleccionado = raster_elevacion_limitado_seleccionado.view(malla_elevacion_planicies_corregida,nodata=np.nan)
    vista_malla_delimitacion_direccion_flujo_seleccionado = raster_elevacion_limitado_seleccionado.view(malla_direccion_flujo,nodata=np.nan)
    vista_malla_delimitacion_acumulacion_flujo_seleccionado = raster_elevacion_limitado_seleccionado.view(malla_acumulacion_flujo,nodata=np.nan)

    raster_elevacion_limitado_maximo.to_raster(vista_malla_delimitacion_flujo_maximo,ruta_archivos_resultados_rasters+'\\'+'RasterCalculadoMaximo.dem.tif')
    raster_elevacion_limitado_seleccionado.to_raster(vista_malla_delimitacion_flujo_maximo,ruta_archivos_resultados_rasters+'\\'+'RasterCalculadoSeleccionado.dem.tif')

    fig4,axis4 = plt.subplots(1,3,figsize=(30,18))
    fig4.patch.set_alpha(0)

    img411=axis4[0].imshow(vista_malla_delimitacion_flujo_maximo
                          ,extent=raster_elevacion_limitado_maximo.extent
                          ,cmap='terrain')
    fig4.colorbar(img411
                 ,ax=axis4[0]
                 ,label='Elevación [metros]')
    axis4[0].set_title('Mapa de elevación digital'
                      ,fontsize=14
                      ,fontweight='bold')
    axis4[0].set_xlabel('Longitud')
    axis4[0].set_ylabel('Latitud')
    axis4[0].grid()

    img412=axis4[1].imshow(vista_malla_delimitacion_direccion_flujo_maximo
                          ,extent=raster_elevacion_limitado_maximo.extent
                          ,cmap='viridis')
    limites412 = ([0] + sorted(list(mapa_coordenado)))
    fig4.colorbar(img412
                 ,boundaries= limites412
                 ,values=sorted(mapa_coordenado)
                 ,ax=axis4[1])
    axis4[1].set_title('Delimitación de dirección de flujo'
                      ,fontsize=14
                      ,fontweight='bold')
    axis4[1].set_xlabel('Longitud')
    axis4[1].set_ylabel('Latitud')
    axis4[1].grid()

    img412=axis4[2].imshow(vista_malla_delimitacion_acumulacion_flujo_maximo
                          ,extent=raster_elevacion_limitado_maximo.extent
                          ,cmap='cubehelix'
                          ,norm=colors.LogNorm(1, malla_acumulacion_flujo.max())
                          ,interpolation='hermite')
    fig4.colorbar(img412
                 ,ax=axis4[2]
                 ,label='Escala de acumulación')
    axis4[2].set_title('Delimitación de acumulación de flujo'
                      ,fontsize=14
                      ,fontweight='bold')
    axis4[2].set_xlabel('Longitud')
    axis4[2].set_ylabel('Latitud')
    axis4[2].grid()

    fig4.tight_layout()
    fig4.savefig(ruta_archivos_resultados_graficas+'\\'+'MapaFlujoCuencaMaxima.png', bbox_inches = "tight")

    fig5,axis5 = plt.subplots(1,3,figsize=(30,7))
    fig5.patch.set_alpha(0)

    img511=axis5[0].imshow(vista_malla_delimitacion_flujo_seleccionado
                          ,extent=raster_elevacion_limitado_seleccionado.extent
                          ,cmap='terrain')
    fig5.colorbar(img511
                 ,ax=axis5[0]
                 ,label='Elevación [metros]')
    axis5[0].set_title('Mapa de elevación digital'
                      ,fontsize=14
                      ,fontweight='bold')
    axis5[0].set_xlabel('Longitud')
    axis5[0].set_ylabel('Latitud')
    axis5[0].grid()

    img512=axis5[1].imshow(vista_malla_delimitacion_direccion_flujo_seleccionado
                          ,extent=raster_elevacion_limitado_seleccionado.extent
                          ,cmap='viridis')
    limites512 = ([0] + sorted(list(mapa_coordenado)))
    fig5.colorbar(img512
                 ,boundaries= limites512
                 ,values=sorted(mapa_coordenado)
                 ,ax=axis5[1])
    axis5[1].set_title('Delimitación de dirección de flujo'
                      ,fontsize=14
                      ,fontweight='bold')
    axis5[1].set_xlabel('Longitud')
    axis5[1].set_ylabel('Latitud')
    axis5[1].grid()

    img513=axis5[2].imshow(vista_malla_delimitacion_acumulacion_flujo_seleccionado
                          ,extent=raster_elevacion_limitado_seleccionado.extent
                          ,cmap='cubehelix'
                          ,norm=colors.LogNorm(1, malla_acumulacion_flujo.max())
                          ,interpolation='hermite')
    fig4.colorbar(img513
                 ,ax=axis5[2]
                 ,label='Escala de acumulación')
    axis5[2].set_title('Delimitación de acumulación de flujo'
                      ,fontsize=14
                      ,fontweight='bold')
    axis5[2].set_xlabel('Longitud')
    axis5[2].set_ylabel('Latitud')
    axis5[2].grid()

    fig5.tight_layout()
    fig5.savefig(ruta_archivos_resultados_graficas+'\\'+'MapaFlujoCuencaSeleccionada.png', bbox_inches = "tight")
    return raster_elevacion_limitado_maximo,vista_malla_delimitacion_flujo_maximo,vista_malla_delimitacion_direccion_flujo_maximo,vista_malla_delimitacion_acumulacion_flujo_maximo,raster_elevacion_limitado_seleccionado,vista_malla_delimitacion_flujo_seleccionado,vista_malla_delimitacion_direccion_flujo_seleccionado,vista_malla_delimitacion_acumulacion_flujo_seleccionado
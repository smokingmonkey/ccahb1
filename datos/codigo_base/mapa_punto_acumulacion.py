###########################################################################################
                                       # Librerías #
###########################################################################################

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import folium
import os
import procesamiento_raster

from folium.plugins import MousePosition

import warnings

warnings.filterwarnings('ignore')
sns.set_palette('husl')

###########################################################################################
                                     # Parámetros generales #
###########################################################################################

mapa_coordenado= procesamiento_raster.mapa_coordenado
ruta_archivos_resultados_mapas=os.path.join(os.getcwd(),'datos\\archivos\\resultados\\mapas\\original')

###########################################################################################
                                # Funciones auxiliares para ejecución#
###########################################################################################

def color_raster_norm(arreglo_raster, cmap='viridis'):
    datos_normalizados = (arreglo_raster-arreglo_raster.min())/(arreglo_raster.max()-arreglo_raster.min())
    cm = plt.cm.get_cmap(cmap)
    return cm(datos_normalizados)

def color_raster_lognorm(arreglo_raster, cmap='cubehelix'):
    datos_normalizados = colors.LogNorm(1, arreglo_raster.max())(arreglo_raster)
    cm = plt.cm.get_cmap(cmap)
    return cm(datos_normalizados)

###########################################################################################
                                       # Algoritmo #
###########################################################################################

def parametros_generales(raster_elevacion,malla_elevacion_planicies_corregida,malla_acumulacion_flujo):
    longitud_raster_minima=raster_elevacion.extent[0]
    longitud_raster_maxima=raster_elevacion.extent[1]

    latitud_raster_minima=raster_elevacion.extent[2]
    latitud_raster_maxima=raster_elevacion.extent[3]

    malla_vector_elevacion=np.array(malla_elevacion_planicies_corregida)
    malla_vector_acumulacion_flujo=np.array(malla_acumulacion_flujo)

    latitud_media=malla_elevacion_planicies_corregida.coords[:,0].mean()
    longitud_media=malla_elevacion_planicies_corregida.coords[:,1].mean()

    punto_principal={'Latitud':latitud_media,'Longitud':longitud_media}
    return punto_principal,longitud_raster_minima,longitud_raster_maxima,latitud_raster_minima,latitud_raster_maxima,longitud_media,latitud_media,malla_vector_elevacion,malla_vector_acumulacion_flujo

def mapa_base(punto_principal,longitud_raster_minima,longitud_raster_maxima,latitud_raster_minima,latitud_raster_maxima,malla_vector_elevacion):
    mapa_base_raster=folium.Map(location=[punto_principal['Latitud'],punto_principal['Longitud']]
                               ,zoom_start=14
                               ,min_zoom=12
                               ,zoom_control=True
                               ,scrollWheelZoom=True
                               ,dragging=True
                               ,min_lat=latitud_raster_minima
                               ,max_lat=latitud_raster_maxima
                               ,min_lon=longitud_raster_minima
                               ,max_lon=longitud_raster_maxima
                               ,max_bounds=True
                               ,tiles='cartodbpositron')
    malla_vector_color_base=color_raster_norm(malla_vector_elevacion, cmap='gray')
    folium.raster_layers.ImageOverlay(image=malla_vector_color_base
                                     ,opacity=0.6
                                     ,bounds=[[latitud_raster_minima, longitud_raster_minima],
                                              [latitud_raster_maxima, longitud_raster_maxima]]).add_to(mapa_base_raster)

    mapa_base_raster.add_child(folium.LatLngPopup())
    formato_coordenadas_simple="function(num) {return L.Util.formatNum(num, 3);};"
    MousePosition(position="topright"
                 ,separator=" | "
                 ,empty_string="NaN"
                 ,lng_first=True
                 ,num_digits=20
                 ,prefix="Coordenadas:"
                 ,lat_formatter=formato_coordenadas_simple
                 ,lng_formatter=formato_coordenadas_simple).add_to(mapa_base_raster)
    mapa_base_raster.save(ruta_archivos_resultados_mapas + '\\' + 'MapaRasterBase.html')

def mapa_simple(punto_principal,longitud_raster_minima,longitud_raster_maxima,latitud_raster_minima,latitud_raster_maxima,malla_vector_acumulacion_flujo):
    mapa_simple=folium.Map(location=[punto_principal['Latitud'],punto_principal['Longitud']]
                          ,zoom_start=14
                          ,min_zoom=12
                          ,zoom_control=True
                          ,scrollWheelZoom=True
                          ,dragging=True
                          ,min_lat=latitud_raster_minima
                          ,max_lat=latitud_raster_maxima
                          ,min_lon=longitud_raster_minima
                          ,max_lon=longitud_raster_maxima
                          ,max_bounds=True
                          ,tiles='cartodbpositron')
    malla_vector_acumulacion_color_simple=color_raster_norm(malla_vector_acumulacion_flujo, cmap='cubehelix')
    folium.raster_layers.ImageOverlay(image=malla_vector_acumulacion_color_simple
                                     ,opacity=0.6
                                     ,bounds=[[latitud_raster_minima, longitud_raster_minima],
                                              [latitud_raster_maxima, longitud_raster_maxima]]).add_to(mapa_simple)

    mapa_simple.add_child(folium.LatLngPopup())
    formato_coordenadas_simple="function(num) {return L.Util.formatNum(num, 3);};"
    MousePosition(position="topright"
                 ,separator=" | "
                 ,empty_string="NaN"
                 ,lng_first=True
                 ,num_digits=20
                 ,prefix="Coordenadas:"
                 ,lat_formatter=formato_coordenadas_simple
                 ,lng_formatter=formato_coordenadas_simple).add_to(mapa_simple)
    mapa_simple.save(ruta_archivos_resultados_mapas + '\\' + 'MapaAcumulacionSimple.html')


def mapa_detalle(punto_principal,longitud_raster_minima,longitud_raster_maxima,latitud_raster_minima,latitud_raster_maxima,malla_vector_acumulacion_flujo):
    mapa_detalle=folium.Map(location=[punto_principal['Latitud'],punto_principal['Longitud']]
                           ,zoom_start=14
                           ,min_zoom=12
                           ,zoom_control=True
                           ,scrollWheelZoom=True
                           ,dragging=True
                           ,min_lat=latitud_raster_minima
                           ,max_lat=latitud_raster_maxima
                           ,min_lon=longitud_raster_minima
                           ,max_lon=longitud_raster_maxima
                           ,max_bounds=True
                           ,tiles='cartodbpositron')

    malla_vector_acumulacion_color_detalle=color_raster_lognorm(malla_vector_acumulacion_flujo, cmap='cubehelix')
    folium.raster_layers.ImageOverlay(image=malla_vector_acumulacion_color_detalle
                                     ,opacity=1.0
                                     ,bounds=[[latitud_raster_minima,longitud_raster_minima]
                                             ,[latitud_raster_maxima,longitud_raster_maxima]]).add_to(mapa_detalle)

    mapa_detalle.add_child(folium.LatLngPopup())
    formato_coordenadas_detalle="function(num) {return L.Util.formatNum(num, 3);};"
    MousePosition(position="topright"
                 ,separator=" | "
                 ,empty_string="NaN"
                 ,lng_first=True
                 ,num_digits=20
                 ,prefix="Coordenadas:"
                 ,lat_formatter=formato_coordenadas_detalle
                 ,lng_formatter=formato_coordenadas_detalle).add_to(mapa_detalle)
    mapa_detalle.save(ruta_archivos_resultados_mapas+'\\'+'MapaAcumulacionDetalle.html')
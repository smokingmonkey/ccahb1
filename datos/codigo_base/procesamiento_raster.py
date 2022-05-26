###########################################################################################
                                       # Librerías #
###########################################################################################

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from pysheds.grid import Grid

import glob
import warnings
import os

warnings.filterwarnings('ignore')
sns.set_palette('husl')

###########################################################################################
                                 # Parámetros generales #
###########################################################################################

mapa_coordenado = (64, 128, 1, 2, 4, 8, 16, 32)
ruta_archivos_resultados_graficas=os.path.join(os.getcwd(),'datos\\archivos\\resultados\\graficas')

###########################################################################################
                                       # Algoritmo #
###########################################################################################

def lectura_raster():
    archivo_raster = max(glob.glob(os.path.join(os.getcwd(),'datos\\archivos\\raster_transformado')+"\\*.dem.tif"), key=os.path.getctime)
    raster_elevacion = Grid.from_raster(archivo_raster)
    malla_elevacion= raster_elevacion.read_raster(archivo_raster)

    fig1, axis1 = plt.subplots(1,2,figsize=(12,7))
    fig1.patch.set_alpha(0)

    img111 = axis1[0].imshow(malla_elevacion
                            ,extent=raster_elevacion.extent
                            ,cmap='terrain'
                            ,zorder=1)
    fig1.colorbar(img111
                 ,ax=axis1[0]
                 ,label='Elevación [metros]')
    axis1[0].set_title('Mapa de elevación digital (Terreno)'
                       ,fontsize=14
                       ,fontweight='bold')
    axis1[0].set_xlabel('Longitud')
    axis1[0].set_ylabel('Latitud')
    axis1[0].tick_params(axis='x'
                        ,which='major'
                        ,pad=15)

    img112 = axis1[1].imshow(malla_elevacion
                            ,extent=raster_elevacion.extent
                            ,cmap='gray'
                            ,zorder=1)
    fig1.colorbar(img112
                 ,ax=axis1[1]
                 ,label='Elevación [metros]')
    axis1[1].set_title('Mapa de elevación digital'
                      ,fontsize=14
                      ,fontweight='bold')
    axis1[1].set_xlabel('Longitud')
    axis1[1].set_ylabel('Latitud')
    axis1[1].tick_params(axis='x'
                        ,which='major'
                        ,pad=15)

    fig1.tight_layout()
    fig1.savefig(ruta_archivos_resultados_graficas+'\\'+'MapaRaster.png', bbox_inches = "tight")
    return raster_elevacion,malla_elevacion

def corregir_raster(raster_elevacion,malla_elevacion):
    malla_huecos=raster_elevacion.detect_pits(malla_elevacion)
    malla_elevacion_huecos_corregida=raster_elevacion.fill_pits(malla_elevacion)

    malla_depresiones = raster_elevacion.detect_depressions(malla_elevacion_huecos_corregida)
    malla_elevacion_depresion_corregida=raster_elevacion.fill_depressions(malla_elevacion_huecos_corregida)

    malla_planicies = raster_elevacion.detect_flats(malla_elevacion_depresion_corregida)
    malla_elevacion_planicies_corregida=raster_elevacion.resolve_flats(malla_elevacion_depresion_corregida)

    fig2, axis2 = plt.subplots(1,3,figsize=(16,7))
    fig2.patch.set_alpha(0)

    img211 = axis2[0].imshow(malla_huecos
                            ,extent=raster_elevacion.extent
                            ,cmap='inferno'
                            ,zorder=2)
    axis2[0].set_title('Malla de huecos del raster'
                      ,fontsize=14
                      ,fontweight='bold')
    axis2[0].tick_params(axis='x'
                        ,which='major'
                        ,pad=15)

    img212 = axis2[1].imshow(malla_depresiones
                            ,extent=raster_elevacion.extent
                            ,cmap='inferno'
                            ,zorder=2)
    axis2[1].set_title('Malla de depresiones del raster'
                      ,fontsize=14
                      ,fontweight='bold')
    axis2[1].tick_params(axis='x'
                        ,which='major'
                        ,pad=15)

    img213 = axis2[2].imshow(malla_planicies
                            ,extent=raster_elevacion.extent
                            ,zorder=2)
    axis2[2].set_title('Malla de planicies del raster'
                      ,fontsize=14
                      ,fontweight='bold')
    axis2[2].tick_params(axis='x'
                        ,which='major'
                        ,pad=15)

    fig2.tight_layout()
    fig2.savefig(ruta_archivos_resultados_graficas+'\\'+'MapaDetalleRaster.png', bbox_inches = "tight")
    return malla_elevacion_planicies_corregida

def procesar_raster(raster_elevacion,malla_elevacion_planicies_corregida):
    malla_direccion_flujo=raster_elevacion.flowdir(malla_elevacion_planicies_corregida
                                                  ,dirmap=mapa_coordenado)
    malla_acumulacion_flujo=raster_elevacion.accumulation(malla_direccion_flujo
                                                         ,dirmap=mapa_coordenado)

    malla_punto_drenaje_alto=raster_elevacion.compute_hand(malla_direccion_flujo
                                                          ,malla_elevacion_planicies_corregida
                                                          ,malla_acumulacion_flujo>=np.percentile(malla_acumulacion_flujo,99.9))

    fig3,axis3 = plt.subplots(1,2,figsize=(12,7))
    fig3.patch.set_alpha(0)

    img311 = axis3[0].imshow(malla_direccion_flujo
                            ,extent=raster_elevacion.extent
                            ,cmap='viridis'
                            ,zorder=2)
    limites311 = ([0] + sorted(list(mapa_coordenado)))
    fig3.colorbar(img311
                 ,boundaries= limites311
                 ,values=sorted(mapa_coordenado)
                 ,ax=axis3[0])
    axis3[0].set_xlabel('Longitud')
    axis3[0].set_ylabel('Latitud')
    axis3[0].set_title('Malla de dirección de flujo'
                       ,fontsize=14
                       ,fontweight='bold')
    axis3[0].grid()
    axis3[0].tick_params(axis='x'
                        ,which='major'
                        ,pad=15)

    img312 = axis3[1].imshow(malla_acumulacion_flujo
                            ,extent=raster_elevacion.extent
                            ,norm=colors.LogNorm(1,malla_acumulacion_flujo.max())
                            ,cmap='cubehelix'
                            ,zorder=2
                            ,interpolation='hermite')
    fig3.colorbar(img312
                 ,ax=axis3[1]
                 ,label='Escala de acumulación')
    axis3[1].set_xlabel('Longitud')
    axis3[1].set_ylabel('Latitud')
    axis3[1].set_title('Mapa de acumulación de flujo'
                      ,fontsize=14
                      ,fontweight='bold')
    axis3[1].grid()
    axis3[1].tick_params(axis='x'
                        ,which='major'
                        ,pad=15)

    fig3.tight_layout()
    fig3.savefig(ruta_archivos_resultados_graficas+'\\'+'MapaFlujoRaster.png', bbox_inches = "tight")
    return malla_direccion_flujo,malla_acumulacion_flujo,malla_punto_drenaje_alto
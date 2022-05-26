###########################################################################################
                                       # Librerías #
###########################################################################################

import shutil
import os
import sys

sys.path.append(os.path.join(sys.path[0],'datos','codigo_base'))


from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import Request
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

import funciones_auxiliares_app
import modelos_app

import transformacion_raster
import procesamiento_raster
import mapa_punto_acumulacion
import delimitacion_cuenca
import procesamiento_cuenca

###########################################################################################
                                  # Funcionales de la API #
###########################################################################################


app=FastAPI()

plantillas_jinja=Jinja2Templates(directory="directorio_html/html")
mapas_jinja=Jinja2Templates(directory="datos/archivos/resultados/mapas/modificado")


app.mount("/resultados", StaticFiles(directory="datos/archivos/resultados/graficas"), name="graficas")
app.mount("/StylesFiles", StaticFiles(directory="FrontEnd/Styles"), name="styles")
app.mount("/JavascriptFiles", StaticFiles(directory="FrontEnd/Javascript"), name="globeJs")

@app.get("/")
async def pagina_base():
    return RedirectResponse("http://127.0.0.1:8000/Principal", status_code=301)

@app.get("/Principal", response_class=HTMLResponse)
async def pagina_principal(request: Request):
    return plantillas_jinja.TemplateResponse("pagina_principal.html", context={"request": request})

@app.get("/pagina_extraccion", response_class=HTMLResponse)
async def pagina_extraccion(request: Request):
    return plantillas_jinja.TemplateResponse("pagina_extraccion.html", context={"request": request})

@app.get("/pagina_carga", response_class=HTMLResponse)
async def pagina_carga(request: Request):
    return plantillas_jinja.TemplateResponse("pagina_carga.html", context={"request": request})

@app.post("/pagina_carga", response_class=HTMLResponse)
async def raster_carga(request: Request,archivo_raster_original: UploadFile=File(...)):
    localizacion_inicial_raster=os.path.join(os.getcwd(), archivo_raster_original.filename)
    localizacion_final_raster =os.path.join(os.getcwd(),'datos\\archivos\\raster_original',archivo_raster_original.filename)
    if archivo_raster_original.filename.endswith('.dem.tif'):
        with open(f'{archivo_raster_original.filename}','wb') as raster_original_memoria:
            shutil.copyfileobj(archivo_raster_original.file,raster_original_memoria)
        shutil.move(localizacion_inicial_raster, localizacion_final_raster)
        return plantillas_jinja.TemplateResponse("pagina_carga_exitosa.html", context={"request": request})
    else:
        return plantillas_jinja.TemplateResponse("pagina_carga_errada.html", context={"request": request})

@app.get("/pagina_transformacion", response_class=HTMLResponse)
async def pagina_transformacion(request: Request):
    return plantillas_jinja.TemplateResponse("pagina_transformacion.html", context={"request": request})

@app.post("/pagina_transformacion")
async def raster_transforma(request: Request):
    raster_transformado=transformacion_raster.transformacion_datos_raster()
    return plantillas_jinja.TemplateResponse("pagina_transformacion_exitosa.html", context={"request": request,'raster_transformado':raster_transformado})

@app.get("/pagina_procesamiento", response_class=HTMLResponse)
async def pagina_procesamiento(request: Request):
    return plantillas_jinja.TemplateResponse("pagina_procesamiento.html", context={"request": request})

@app.post("/pagina_procesamiento", response_class=HTMLResponse)
async def raster_procesa(request: Request):
    raster_cargado=procesamiento_raster.lectura_raster()
    raster_corregido=procesamiento_raster.corregir_raster(raster_cargado[0],raster_cargado[1])
    raster_procesado=procesamiento_raster.procesar_raster(raster_cargado[0],raster_corregido)
    parametros_mapas=mapa_punto_acumulacion.parametros_generales(raster_cargado[0],raster_corregido,raster_procesado[1])
    mapa_base=mapa_punto_acumulacion.mapa_base(parametros_mapas[0],parametros_mapas[1],parametros_mapas[2],parametros_mapas[3],parametros_mapas[4],parametros_mapas[7])
    mapa_simple=mapa_punto_acumulacion.mapa_simple(parametros_mapas[0],parametros_mapas[1],parametros_mapas[2],parametros_mapas[3],parametros_mapas[4],parametros_mapas[8])
    mapa_detalle=mapa_punto_acumulacion.mapa_detalle(parametros_mapas[0],parametros_mapas[1],parametros_mapas[2],parametros_mapas[3],parametros_mapas[4],parametros_mapas[8])
    return plantillas_jinja.TemplateResponse("pagina_procesamiento_exitoso.html", context={"request": request})

@app.get("/pagina_mapas", response_class=HTMLResponse)
async def pagina_mapas(request: Request):
    html_formulario_mapa_base = """
            <form display="none" id="mapa_simple" name="formulario_mapa_base" action="mapa_raster_base" method="post" autocomplete="off" enctype="multipart/form-data">
            <input type="text" name="latitud" value="0"/>
            <input type="text" name="longitud" value="0"/>
            <input type="submit">
            </form>
            """
    html_formulario_mapa_simple = """
        <form display="none" id="mapa_simple" name="formulario_mapa_simple" action="mapa_acumulacion_simple" method="post" autocomplete="off" enctype="multipart/form-data">
        <input type="text" name="latitud" value="0"/>
        <input type="text" name="longitud" value="0"/>
        <input type="submit">
        </form>
        """
    html_formulario_mapa_detalle = """
        <form display="none" id="mapa_simple" name="formulario_mapa_detalle" action="mapa_acumulacion_detalle" method="post" autocomplete="off" enctype="multipart/form-data">
        <input type="text" name="latitud" value="0"/>
        <input type="text" name="longitud" value="0"/>
        <input type="submit">
        </form>
        """
    html_script_click = """
    var id_mapa_simple=document.querySelector('.folium-map').id
    window[id_mapa_simple].on('click', sendTest);
    function sendTest(e)
    {
    let latitud = document.querySelector('input[name="latitud"]');
    latitud.value = e.latlng.lat;

    let longitud = document.querySelector('input[name="longitud"]');
    longitud.value = e.latlng.lng;

    let forms = document.querySelector('form[name="formulario_mapa_simple"]');
    forms.submit();}"""
    funciones_auxiliares_app.insertar_html_cuerpo(html_formulario_mapa_base,'datos\\archivos\\resultados\\mapas\\original\\MapaRasterBase.html','datos\\archivos\\resultados\\mapas\\modificado\\MapaRasterBase.html')
    funciones_auxiliares_app.insertar_html_cuerpo(html_formulario_mapa_simple,'datos\\archivos\\resultados\\mapas\\original\\MapaAcumulacionSimple.html','datos\\archivos\\resultados\\mapas\\modificado\\MapaAcumulacionSimple.html')
    funciones_auxiliares_app.insertar_html_cuerpo(html_formulario_mapa_detalle,'datos\\archivos\\resultados\\mapas\\original\\MapaAcumulacionDetalle.html','datos\\archivos\\resultados\\mapas\\modificado\\MapaAcumulacionDetalle.html')
    funciones_auxiliares_app.insertar_script_html_final(html_script_click,'datos\\archivos\\resultados\\mapas\\modificado\\MapaRasterBase.html','datos\\archivos\\resultados\\mapas\\modificado\\MapaRasterBase.html')
    funciones_auxiliares_app.insertar_script_html_final(html_script_click,'datos\\archivos\\resultados\\mapas\\modificado\\MapaAcumulacionSimple.html','datos\\archivos\\resultados\\mapas\\modificado\\MapaAcumulacionSimple.html')
    funciones_auxiliares_app.insertar_script_html_final(html_script_click,'datos\\archivos\\resultados\\mapas\\modificado\\MapaAcumulacionDetalle.html','datos\\archivos\\resultados\\mapas\\modificado\\MapaAcumulacionDetalle.html')
    return plantillas_jinja.TemplateResponse("pagina_mapas.html",context={"request": request})

@app.get("/mapa_raster_base", response_class=HTMLResponse)
async def pagina_mapa_base(request: Request):
    return mapas_jinja.TemplateResponse("MapaRasterBase.html",context={"request": request})

@app.get("/mapa_acumulacion_simple", response_class=HTMLResponse)
async def pagina_mapa_simple(request: Request):
    return mapas_jinja.TemplateResponse("MapaAcumulacionSimple.html",context={"request": request})

@app.post("/mapa_acumulacion_simple", response_class=HTMLResponse)
async def punto_mapa_simple(request: Request,coordenadas_click_acumulacion:modelos_app.coordenadas_click=Depends(modelos_app.coordenadas_click.tipo_formulario)):
    raster_cargado = procesamiento_raster.lectura_raster()
    raster_corregido = procesamiento_raster.corregir_raster(raster_cargado[0], raster_cargado[1])
    raster_procesado = procesamiento_raster.procesar_raster(raster_cargado[0], raster_corregido)
    cuenca_delimitada = delimitacion_cuenca.limites_cuenca(raster_cargado[0], raster_procesado[0], raster_procesado[1],
                                                           coordenadas_click_acumulacion.longitud, coordenadas_click_acumulacion.latitud)
    cuenca_procesada = delimitacion_cuenca.procesamiento_cuenca(raster_cargado[0], raster_corregido,
                                                                raster_procesado[0], raster_procesado[1],
                                                                cuenca_delimitada[0], cuenca_delimitada[1])
    cuenca_drenaje = procesamiento_cuenca.procesamiento_red_drenaje(raster_procesado[0], raster_procesado[1],
                                                                    cuenca_procesada[0], cuenca_procesada[4])
    cuenca_inundacion = procesamiento_cuenca.procesamiento_red_inundacion(raster_procesado[2], cuenca_procesada[0],
                                                                          cuenca_procesada[4])
    return plantillas_jinja.TemplateResponse("pagina_delimitacion_cuenca_exitosa.html",context={"request": request,'coordenadas_click_acumulacion':coordenadas_click_acumulacion})

@app.get("/resultados_cuenca", response_class=HTMLResponse)
async def pagina_resultados_cuenca(request: Request):
    return plantillas_jinja.TemplateResponse("pagina_resultados_cuenca.html",context={"request": request})

@app.get("/mapa_acumulacion_detalle", response_class=HTMLResponse)
async def pagina_mapa_detalle(request: Request):
    return mapas_jinja.TemplateResponse("MapaAcumulacionDetalle.html",context={"request": request})

@app.post("/mapa_acumulacion_detalle", response_class=HTMLResponse)
async def punto_mapa_detalle(request: Request):
    return mapas_jinja.TemplateResponse("pagina_delimitacion_cuenca.html",context={"request": request})
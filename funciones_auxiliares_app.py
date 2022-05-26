###########################################################################################
                                       # Librerías #
###########################################################################################

import bs4

###########################################################################################
                                  # Funciones de aplicación #
###########################################################################################

def insertar_html_cuerpo(htlm_insertar,html_original,html_nuevo):
    with open(html_original) as mapa_simple_original:
        html_mapa_simple_original = mapa_simple_original.read()
        bfs_mapa_simple_original = bs4.BeautifulSoup(html_mapa_simple_original,'html.parser')
    bfs_mapa_simple_original.body.append(bs4.BeautifulSoup(htlm_insertar))
    with open(html_nuevo, "w") as mapa_simple_nuevo:
        mapa_simple_nuevo.write(str(bfs_mapa_simple_original))

def insertar_script_html_final(script_crudo,html_original,html_nuevo):
    with open(html_original) as mapa_simple_original:
        html_mapa_simple_original = mapa_simple_original.read()
        bfs_mapa_simple_original = bs4.BeautifulSoup(html_mapa_simple_original)
    funcion_click = bfs_mapa_simple_original.new_tag('script')
    funcion_click.string=script_crudo
    bfs_mapa_simple_original.append(funcion_click)
    with open(html_nuevo, "w") as mapa_simple_nuevo:
        mapa_simple_nuevo.write(str(bfs_mapa_simple_original))
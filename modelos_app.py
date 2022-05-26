###########################################################################################
                                       # Librerías #
###########################################################################################

from fastapi import Form
from pydantic import BaseModel

###########################################################################################
                                   # Modelos de la API #
###########################################################################################

class coordenadas_click(BaseModel):
    latitud:float
    longitud:float
    @classmethod
    def tipo_formulario(cls,
                        latitud:float=Form(...),
                        longitud:float=Form(...)):
        return cls(latitud=latitud,
                   longitud=longitud)
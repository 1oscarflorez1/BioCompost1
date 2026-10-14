from datetime import date

from pydantic import BaseModel, ConfigDict, model_validator


class EsquemaEntrada(BaseModel):
    """Base para los datos que llegan del frontend.

    - Quita espacios al inicio y al final de los textos.
    - Convierte los textos vacíos ("") en null, para que los campos opcionales
      de los formularios lleguen como nulos y los obligatorios fallen con un
      mensaje claro.
    """

    model_config = ConfigDict(use_enum_values=True, str_strip_whitespace=True)

    @model_validator(mode="before")
    @classmethod
    def _vacios_a_nulo(cls, datos):
        if isinstance(datos, dict):
            return {k: (None if isinstance(v, str) and not v.strip() else v) for k, v in datos.items()}
        return datos


def fecha_no_futura(valor: date | None) -> date | None:
    if valor and valor > date.today():
        raise ValueError("La fecha no puede ser posterior a hoy")
    return valor


class Mensaje(BaseModel):
    mensaje: str

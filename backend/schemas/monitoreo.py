from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from schemas.base import EsquemaEntrada, fecha_no_futura


class MonitoreoEntrada(EsquemaEntrada):
    id_pila: int = Field(gt=0)
    fecha_monitoreo: date
    temperatura: float = Field(ge=0, le=90, description="Grados Celsius")
    humedad: float = Field(ge=0, le=100, description="Porcentaje de humedad")
    ph: float | None = Field(default=None, ge=0, le=14)
    volteo: Literal["S", "N"] = Field(default="N", description="S si se volteó la pila en esta visita")
    observaciones: str | None = Field(default=None, max_length=400)

    _fecha = field_validator("fecha_monitoreo")(fecha_no_futura)


class MonitoreoRespuesta(BaseModel):
    id_monitoreo: int
    id_pila: int
    pila: str
    fase: str
    id_usuario: int
    usuario: str
    fecha_monitoreo: date
    temperatura: float
    humedad: float
    ph: float | None
    volteo: str
    observaciones: str | None
    alerta: str | None = None

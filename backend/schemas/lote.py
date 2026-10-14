from datetime import date

from pydantic import BaseModel, Field, field_validator

from models.catalogos import CalidadLote, EstadoLote
from schemas.base import EsquemaEntrada, fecha_no_futura


class LoteEntrada(EsquemaEntrada):
    id_pila: int = Field(gt=0, description="Pila de la que proviene el abono")
    codigo_lote: str = Field(min_length=3, max_length=20, pattern=r"^[A-Za-z0-9-]+$", examples=["L-2026-005"])
    fecha_produccion: date
    kilos_producidos: float = Field(gt=0, le=100000)
    calidad: CalidadLote = CalidadLote.ESTANDAR
    estado: EstadoLote = EstadoLote.DISPONIBLE
    observaciones: str | None = Field(default=None, max_length=400)

    _fecha = field_validator("fecha_produccion")(fecha_no_futura)

    @field_validator("codigo_lote")
    @classmethod
    def codigo_en_mayusculas(cls, valor: str) -> str:
        return valor.upper()


class LoteRespuesta(BaseModel):
    id_lote: int
    id_pila: int
    pila: str
    codigo_lote: str
    fecha_produccion: date
    kilos_producidos: float
    calidad: str
    estado: str
    observaciones: str | None

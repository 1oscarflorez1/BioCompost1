from datetime import date

from pydantic import BaseModel, Field, field_validator, model_validator

from models.catalogos import FasePila
from schemas.base import EsquemaEntrada, fecha_no_futura


class PilaEntrada(EsquemaEntrada):
    codigo: str = Field(min_length=3, max_length=20, pattern=r"^[A-Za-z0-9-]+$", examples=["P-2026-07"])
    ubicacion: str | None = Field(default=None, max_length=100)
    fecha_inicio: date
    fecha_fin: date | None = Field(default=None, description="Obligatoria cuando la fase es FINALIZADA")
    fase: FasePila = FasePila.MESOFILICA
    capacidad_kg: float | None = Field(default=None, gt=0, le=100000)
    observaciones: str | None = Field(default=None, max_length=400)

    _fechas = field_validator("fecha_inicio", "fecha_fin")(fecha_no_futura)

    @field_validator("codigo")
    @classmethod
    def codigo_en_mayusculas(cls, valor: str) -> str:
        return valor.upper()

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValueError("La fecha de finalización no puede ser anterior a la fecha de inicio")
        if self.fase == FasePila.FINALIZADA and not self.fecha_fin:
            raise ValueError("Para finalizar la pila debe indicar la fecha de finalización")
        if self.fase != FasePila.FINALIZADA and self.fecha_fin:
            raise ValueError("Solo una pila en fase FINALIZADA puede tener fecha de finalización")
        return self


class PilaRespuesta(BaseModel):
    id_pila: int
    codigo: str
    ubicacion: str | None
    fecha_inicio: date
    fecha_fin: date | None
    fase: str
    capacidad_kg: float | None
    observaciones: str | None
    kg_recibidos: float
    num_recolecciones: int
    kg_abono: float
    dias_proceso: int
    ultimo_monitoreo: date | None
    ultima_temperatura: float | None
    ultima_humedad: float | None
    alerta: str | None = None

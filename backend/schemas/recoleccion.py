from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from models.catalogos import Clasificacion, TipoResiduo
from schemas.base import EsquemaEntrada, fecha_no_futura


class RecoleccionEntrada(EsquemaEntrada):
    id_proveedor: int = Field(gt=0, description="Proveedor / punto de origen del residuo")
    id_pila: int | None = Field(default=None, gt=0, description="Pila a la que se destina (opcional)")
    fecha_recoleccion: date
    peso_kg: float = Field(gt=0, le=50000, description="Peso registrado en báscula, en kilogramos")
    tipo_residuo: TipoResiduo
    clasificacion: Clasificacion = Clasificacion.APTO
    observaciones: str | None = Field(default=None, max_length=400)

    _fecha = field_validator("fecha_recoleccion")(fecha_no_futura)

    @model_validator(mode="after")
    def validar_clasificacion(self):
        if self.clasificacion == Clasificacion.RECHAZADO and self.id_pila is not None:
            raise ValueError("Un residuo RECHAZADO no puede asignarse a una pila de compostaje")
        if self.clasificacion != Clasificacion.APTO and not self.observaciones:
            raise ValueError("Indique en observaciones el motivo de la clasificación CONDICIONADO o RECHAZADO")
        return self


class RecoleccionRespuesta(BaseModel):
    id_recoleccion: int
    id_proveedor: int
    proveedor: str
    municipio: str
    id_usuario: int
    recolector: str
    id_pila: int | None
    pila: str | None
    fecha_recoleccion: date
    peso_kg: float
    tipo_residuo: str
    clasificacion: str
    observaciones: str | None
    fecha_registro: datetime

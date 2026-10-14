from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from models.catalogos import TipoProveedor, TipoResiduo
from schemas.base import EsquemaEntrada


class ProveedorEntrada(EsquemaEntrada):
    nombre: str = Field(min_length=3, max_length=120, examples=["Plaza de Mercado El Porvenir"])
    tipo_proveedor: TipoProveedor
    documento: str = Field(pattern=r"^[0-9]{5,12}(-[0-9])?$", description="NIT o cédula, ej. 900123456-1")
    contacto: str | None = Field(default=None, max_length=100)
    telefono: str | None = Field(default=None, pattern=r"^[0-9+ ]{7,20}$")
    direccion: str = Field(min_length=5, max_length=200, description="Dirección del punto de recolección")
    municipio: str = Field(min_length=3, max_length=60)
    tipo_residuo: TipoResiduo = Field(description="Tipo de residuo que genera principalmente")
    activo: Literal["S", "N"] = "S"


class ProveedorRespuesta(BaseModel):
    id_proveedor: int
    nombre: str
    tipo_proveedor: str
    documento: str
    contacto: str | None
    telefono: str | None
    direccion: str
    municipio: str
    tipo_residuo: str
    activo: str
    fecha_registro: datetime
    num_recolecciones: int
    kg_aportados: float

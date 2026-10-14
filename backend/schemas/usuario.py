from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

from schemas.base import EsquemaEntrada


def _validar_contrasena(valor: str | None) -> str | None:
    if valor is not None and not (any(c.isalpha() for c in valor) and any(c.isdigit() for c in valor)):
        raise ValueError("La contraseña debe contener letras y números")
    return valor


class UsuarioBase(EsquemaEntrada):
    nombre: str = Field(min_length=3, max_length=100)
    correo: EmailStr
    telefono: str | None = Field(default=None, pattern=r"^[0-9+ ]{7,20}$")
    id_rol: int = Field(gt=0)
    activo: Literal["S", "N"] = "S"


class UsuarioCrear(UsuarioBase):
    contrasena: str = Field(min_length=8, max_length=50)

    _contrasena = field_validator("contrasena")(_validar_contrasena)


class UsuarioActualizar(UsuarioBase):
    contrasena: str | None = Field(
        default=None, min_length=8, max_length=50, description="Dejar vacío para conservar la contraseña actual"
    )

    _contrasena = field_validator("contrasena")(_validar_contrasena)


class UsuarioRespuesta(BaseModel):
    id_usuario: int
    nombre: str
    correo: str
    telefono: str | None
    id_rol: int
    rol: str
    rol_nombre: str
    activo: str
    fecha_creacion: datetime


class RolActualizar(EsquemaEntrada):
    """Solo se editan el nombre visible y la descripción; el código interno es fijo."""

    nombre: str = Field(min_length=3, max_length=50, examples=["Jefe de planta"])
    descripcion: str | None = Field(default=None, max_length=200)


class RolRespuesta(BaseModel):
    id_rol: int
    codigo: str
    nombre: str
    descripcion: str | None
    total_usuarios: int

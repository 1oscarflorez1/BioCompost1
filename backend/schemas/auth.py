from pydantic import BaseModel, EmailStr, Field


class LoginEntrada(BaseModel):
    correo: EmailStr = Field(examples=["admin@biocompost.com"])
    contrasena: str = Field(min_length=1, max_length=50)


class UsuarioSesion(BaseModel):
    id_usuario: int
    nombre: str
    correo: str
    rol: str = Field(description="Código interno del rol: ADMINISTRADOR o RECOLECTOR")
    rol_nombre: str = Field(description="Nombre visible del rol")


class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioSesion

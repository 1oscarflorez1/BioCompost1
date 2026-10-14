"""Dependencias de seguridad que usan los routers.

- usuario_actual: exige un token JWT válido (si no, 401).
- requiere_rol(...): además exige que el usuario tenga uno de los roles (si no, 403).
"""
import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.errores import NoAutorizado, Prohibido
from core.security import decodificar_token
from models.catalogos import Rol
from services import auth_service

esquema_bearer = HTTPBearer(auto_error=False, description="Token JWT obtenido en POST /api/auth/login")

RESPUESTAS_COMUNES = {
    401: {"description": "No ha iniciado sesión o el token es inválido / expiró"},
    403: {"description": "Su rol no tiene permiso para esta acción"},
}


def usuario_actual(credenciales: HTTPAuthorizationCredentials | None = Depends(esquema_bearer)) -> dict:
    if credenciales is None:
        raise NoAutorizado("Debe iniciar sesión para acceder a este recurso")
    try:
        datos = decodificar_token(credenciales.credentials)
    except jwt.ExpiredSignatureError:
        raise NoAutorizado("La sesión expiró. Inicie sesión nuevamente")
    except jwt.InvalidTokenError:
        raise NoAutorizado("Token de acceso inválido")

    # Se consulta el usuario en cada petición: si lo desactivan, pierde el acceso de inmediato
    usuario = auth_service.obtener_usuario_sesion(int(datos["sub"]))
    if not usuario or usuario["activo"] != "S":
        raise NoAutorizado("El usuario no existe o está inactivo")
    return usuario


def requiere_rol(*roles: Rol):
    permitidos = {rol.value for rol in roles}

    def verificar(usuario: dict = Depends(usuario_actual)) -> dict:
        if usuario["rol"] not in permitidos:
            raise Prohibido("No tiene permisos para realizar esta acción")
        return usuario

    return verificar


solo_administrador = requiere_rol(Rol.ADMINISTRADOR)

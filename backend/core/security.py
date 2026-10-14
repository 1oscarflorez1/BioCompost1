"""Funciones de seguridad: cifrado de contraseñas (bcrypt) y tokens JWT."""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from core import config


def cifrar_contrasena(contrasena: str) -> str:
    return bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_contrasena(contrasena: str, contrasena_hash: str) -> bool:
    try:
        return bcrypt.checkpw(contrasena.encode("utf-8"), contrasena_hash.encode("utf-8"))
    except ValueError:
        return False


def crear_token(usuario: dict) -> str:
    ahora = datetime.now(timezone.utc)
    datos = {
        "sub": str(usuario["id_usuario"]),
        "nombre": usuario["nombre"],
        "rol": usuario["rol"],
        "iat": ahora,
        "exp": ahora + timedelta(minutes=config.JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(datos, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


def decodificar_token(token: str) -> dict:
    """Valida firma y expiración. Lanza jwt.InvalidTokenError si el token no es válido."""
    return jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])

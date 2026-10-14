"""Configuración de la aplicación leída desde variables de entorno.

Las credenciales NUNCA se escriben en el código: se leen del archivo .env
(ubicado en la raíz del repositorio) o de las variables del sistema.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR.parent / ".env")  # .env en la raíz del repositorio
load_dotenv(BACKEND_DIR / ".env")  # alternativa: .env dentro de backend/


def _requerida(nombre: str) -> str:
    valor = os.getenv(nombre)
    if not valor:
        raise RuntimeError(
            f"Falta la variable de entorno {nombre}. Copie .env.example como .env y complete los valores."
        )
    return valor


# Base de datos Oracle
DB_USER = _requerida("DB_USER")
DB_PASSWORD = _requerida("DB_PASSWORD")
DB_DSN = os.getenv("DB_DSN", "localhost:1521/FREEPDB1")

# Seguridad (JWT)
JWT_SECRET = _requerida("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "480"))

# Orígenes del frontend autorizados a consumir la API (CORS)
CORS_ORIGINS = [
    origen.strip()
    for origen in os.getenv("CORS_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500").split(",")
    if origen.strip()
]

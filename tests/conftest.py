"""Configuración de las pruebas.

Las pruebas son de integración: usan la API real conectada a Oracle con los
datos de database/03_data.sql. Antes de ejecutarlas:
    1. La base de datos debe estar en ejecución (docker compose up -d).
    2. Los datos iniciales deben estar cargados (python backend/init_db.py).

Ejecutar desde la raíz del repositorio:
    backend/.venv/Scripts/python -m pytest tests -v
"""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from main import app  # noqa: E402

# Usuarios de prueba definidos en database/03_data.sql
ADMIN = {"correo": "admin@biocompost.com", "contrasena": "Admin2026*"}
RECOLECTOR = {"correo": "carlos.rodriguez@biocompost.com", "contrasena": "Recolector2026*"}
INACTIVO = {"correo": "pedro.salazar@biocompost.com", "contrasena": "Recolector2026*"}


@pytest.fixture(scope="session")
def cliente():
    with TestClient(app) as c:
        yield c


def _cabeceras(cliente, credenciales):
    respuesta = cliente.post("/api/auth/login", json=credenciales)
    assert respuesta.status_code == 200, respuesta.text
    return {"Authorization": f"Bearer {respuesta.json()['access_token']}"}


@pytest.fixture(scope="session")
def admin(cliente):
    return _cabeceras(cliente, ADMIN)


@pytest.fixture(scope="session")
def recolector(cliente):
    return _cabeceras(cliente, RECOLECTOR)

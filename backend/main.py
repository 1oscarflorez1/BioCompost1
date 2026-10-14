"""BioCompost API - Sistema de Trazabilidad de Residuos Orgánicos y Compostaje Agrícola.

Ejecutar desde la carpeta backend:
    uvicorn main:app --reload
Documentación interactiva (Swagger): http://127.0.0.1:8000/docs
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core import config
from core.errores import registrar_manejadores
from database.connection import cerrar_pool, consultar_uno, iniciar_pool
from routers import auth, lotes, monitoreos, pilas, proveedores, recolecciones, reportes, usuarios

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    iniciar_pool()
    yield
    cerrar_pool()


app = FastAPI(
    title="BioCompost API",
    version="1.0.0",
    description=(
        "API REST para la trazabilidad de la recolección de residuos orgánicos y su transformación "
        "en abono orgánico.\n\n"
        "**Cómo probar:** ejecute `POST /api/auth/login`, copie el `access_token`, "
        "pulse **Authorize** y péguelo. Roles: `ADMINISTRADOR` y `RECOLECTOR`."
    ),
    lifespan=ciclo_de_vida,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

registrar_manejadores(app)

app.include_router(auth.router)
app.include_router(usuarios.router_roles)
app.include_router(usuarios.router)
app.include_router(proveedores.router)
app.include_router(recolecciones.router)
app.include_router(pilas.router)
app.include_router(monitoreos.router)
app.include_router(lotes.router)
app.include_router(reportes.router)


@app.get("/", tags=["General"], summary="Información de la API")
def inicio():
    return {"mensaje": "API de BioCompost en funcionamiento", "documentacion": "/docs"}


@app.get("/api/salud", tags=["General"], summary="Estado de la API y de la conexión con Oracle")
def salud():
    try:
        consultar_uno("SELECT 1 AS ok FROM dual")
        return {"api": "ok", "base_datos": "ok"}
    except Exception:
        return JSONResponse(status_code=503, content={"api": "ok", "base_datos": "sin conexión"})

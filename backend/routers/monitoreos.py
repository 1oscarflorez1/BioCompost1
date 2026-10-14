from datetime import date

from fastapi import APIRouter, Depends, Query, status

from routers.dependencias import RESPUESTAS_COMUNES, solo_administrador, usuario_actual
from schemas.base import Mensaje
from schemas.monitoreo import MonitoreoEntrada, MonitoreoRespuesta
from services import monitoreos_service

router = APIRouter(prefix="/api/monitoreos", tags=["Pilas de compostaje"], responses=RESPUESTAS_COMUNES)


@router.get("", response_model=list[MonitoreoRespuesta], summary="Listar mediciones de las pilas")
def listar(
    id_pila: int | None = None,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
    solo_alertas: bool = Query(False, description="Solo mediciones fuera de rango"),
    _: dict = Depends(usuario_actual),
):
    return monitoreos_service.listar(id_pila, fecha_desde, fecha_hasta, solo_alertas)


@router.get("/{id_monitoreo}", response_model=MonitoreoRespuesta, summary="Consultar una medición")
def obtener(id_monitoreo: int, _: dict = Depends(usuario_actual)):
    return monitoreos_service.obtener(id_monitoreo)


@router.post(
    "", response_model=MonitoreoRespuesta, status_code=status.HTTP_201_CREATED, summary="Registrar medición"
)
def crear(datos: MonitoreoEntrada, usuario: dict = Depends(solo_administrador)):
    return monitoreos_service.crear(datos, usuario)


@router.put("/{id_monitoreo}", response_model=MonitoreoRespuesta, summary="Actualizar medición")
def actualizar(id_monitoreo: int, datos: MonitoreoEntrada, _: dict = Depends(solo_administrador)):
    return monitoreos_service.actualizar(id_monitoreo, datos)


@router.delete("/{id_monitoreo}", response_model=Mensaje, summary="Eliminar medición")
def eliminar(id_monitoreo: int, _: dict = Depends(solo_administrador)):
    monitoreos_service.eliminar(id_monitoreo)
    return {"mensaje": "Medición eliminada correctamente"}

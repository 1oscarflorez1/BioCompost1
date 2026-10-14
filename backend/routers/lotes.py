from fastapi import APIRouter, Depends, Query, status

from models.catalogos import CalidadLote, EstadoLote
from routers.dependencias import RESPUESTAS_COMUNES, solo_administrador, usuario_actual
from schemas.base import Mensaje
from schemas.lote import LoteEntrada, LoteRespuesta
from services import lotes_service

router = APIRouter(prefix="/api/lotes", tags=["Lotes de abono"], responses=RESPUESTAS_COMUNES)


@router.get("", response_model=list[LoteRespuesta], summary="Listar y filtrar lotes de abono")
def listar(
    texto: str | None = Query(None, description="Busca por código de lote o de pila"),
    estado: EstadoLote | None = None,
    calidad: CalidadLote | None = None,
    id_pila: int | None = None,
    _: dict = Depends(usuario_actual),
):
    return lotes_service.listar(texto, estado, calidad, id_pila)


@router.get("/{id_lote}", response_model=LoteRespuesta, summary="Consultar un lote")
def obtener(id_lote: int, _: dict = Depends(usuario_actual)):
    return lotes_service.obtener(id_lote)


@router.get("/{id_lote}/trazabilidad", summary="Trazabilidad del lote (pila y proveedores de origen)")
def trazabilidad(id_lote: int, _: dict = Depends(usuario_actual)):
    return lotes_service.trazabilidad(id_lote)


@router.post("", response_model=LoteRespuesta, status_code=status.HTTP_201_CREATED, summary="Registrar lote")
def crear(datos: LoteEntrada, _: dict = Depends(solo_administrador)):
    return lotes_service.crear(datos)


@router.put("/{id_lote}", response_model=LoteRespuesta, summary="Actualizar lote")
def actualizar(id_lote: int, datos: LoteEntrada, _: dict = Depends(solo_administrador)):
    return lotes_service.actualizar(id_lote, datos)


@router.delete("/{id_lote}", response_model=Mensaje, summary="Eliminar lote")
def eliminar(id_lote: int, _: dict = Depends(solo_administrador)):
    lotes_service.eliminar(id_lote)
    return {"mensaje": "Lote eliminado correctamente"}

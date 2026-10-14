from fastapi import APIRouter, Depends, Query, status

from models.catalogos import FasePila
from routers.dependencias import RESPUESTAS_COMUNES, solo_administrador, usuario_actual
from schemas.base import Mensaje
from schemas.pila import PilaEntrada, PilaRespuesta
from services import pilas_service

router = APIRouter(prefix="/api/pilas", tags=["Pilas de compostaje"], responses=RESPUESTAS_COMUNES)


@router.get("", response_model=list[PilaRespuesta], summary="Listar pilas y filtrar por fase de maduración")
def listar(
    fase: FasePila | None = Query(None, description="Filtra por fase de maduración"),
    texto: str | None = Query(None, description="Busca por código o ubicación"),
    solo_activas: bool = Query(False, description="Excluye las pilas FINALIZADAS"),
    _: dict = Depends(usuario_actual),
):
    return pilas_service.listar(fase, texto, solo_activas)


@router.get("/{id_pila}", response_model=PilaRespuesta, summary="Consultar una pila")
def obtener(id_pila: int, _: dict = Depends(usuario_actual)):
    return pilas_service.obtener(id_pila)


@router.post("", response_model=PilaRespuesta, status_code=status.HTTP_201_CREATED, summary="Crear pila")
def crear(datos: PilaEntrada, _: dict = Depends(solo_administrador)):
    return pilas_service.crear(datos)


@router.put("/{id_pila}", response_model=PilaRespuesta, summary="Actualizar pila (cambiar fase, cerrar)")
def actualizar(id_pila: int, datos: PilaEntrada, _: dict = Depends(solo_administrador)):
    return pilas_service.actualizar(id_pila, datos)


@router.delete("/{id_pila}", response_model=Mensaje, summary="Eliminar pila")
def eliminar(id_pila: int, _: dict = Depends(solo_administrador)):
    """Elimina también sus monitoreos; las recolecciones quedan sin pila asignada.
    No se permite si la pila ya produjo lotes de abono."""
    pilas_service.eliminar(id_pila)
    return {"mensaje": "Pila eliminada correctamente"}

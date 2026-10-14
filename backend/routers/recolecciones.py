from datetime import date

from fastapi import APIRouter, Depends, Query, status

from models.catalogos import Clasificacion, TipoResiduo
from routers.dependencias import RESPUESTAS_COMUNES, solo_administrador, usuario_actual
from schemas.base import Mensaje
from schemas.recoleccion import RecoleccionEntrada, RecoleccionRespuesta
from services import recolecciones_service

router = APIRouter(prefix="/api/recolecciones", tags=["Recolecciones"], responses=RESPUESTAS_COMUNES)


@router.get("", response_model=list[RecoleccionRespuesta], summary="Listar y filtrar recolecciones")
def listar(
    texto: str | None = Query(None, description="Busca por nombre del proveedor o municipio"),
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
    id_proveedor: int | None = None,
    id_pila: int | None = None,
    tipo_residuo: TipoResiduo | None = None,
    clasificacion: Clasificacion | None = None,
    sin_pila: bool = Query(False, description="Solo entradas aprovechables aún sin pila asignada"),
    _: dict = Depends(usuario_actual),
):
    return recolecciones_service.listar(
        texto, fecha_desde, fecha_hasta, id_proveedor, id_pila, tipo_residuo, clasificacion, sin_pila
    )


@router.get("/{id_recoleccion}", response_model=RecoleccionRespuesta, summary="Consultar una recolección")
def obtener(id_recoleccion: int, _: dict = Depends(usuario_actual)):
    return recolecciones_service.obtener(id_recoleccion)


@router.post(
    "", response_model=RecoleccionRespuesta, status_code=status.HTTP_201_CREATED, summary="Registrar recolección"
)
def crear(datos: RecoleccionEntrada, usuario: dict = Depends(usuario_actual)):
    """Registra una entrada de residuo. El recolector queda asociado al usuario de la sesión."""
    return recolecciones_service.crear(datos, usuario)


@router.put("/{id_recoleccion}", response_model=RecoleccionRespuesta, summary="Actualizar recolección")
def actualizar(id_recoleccion: int, datos: RecoleccionEntrada, usuario: dict = Depends(usuario_actual)):
    """El RECOLECTOR solo puede modificar las recolecciones que él mismo registró."""
    return recolecciones_service.actualizar(id_recoleccion, datos, usuario)


@router.delete("/{id_recoleccion}", response_model=Mensaje, summary="Eliminar recolección")
def eliminar(id_recoleccion: int, _: dict = Depends(solo_administrador)):
    recolecciones_service.eliminar(id_recoleccion)
    return {"mensaje": "Recolección eliminada correctamente"}

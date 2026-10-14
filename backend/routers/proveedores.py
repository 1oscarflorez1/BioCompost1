from typing import Literal

from fastapi import APIRouter, Depends, Query, status

from models.catalogos import TipoProveedor, TipoResiduo
from routers.dependencias import RESPUESTAS_COMUNES, solo_administrador, usuario_actual
from schemas.base import Mensaje
from schemas.proveedor import ProveedorEntrada, ProveedorRespuesta
from services import proveedores_service

router = APIRouter(prefix="/api/proveedores", tags=["Proveedores"], responses=RESPUESTAS_COMUNES)


@router.get("", response_model=list[ProveedorRespuesta], summary="Listar, buscar y filtrar proveedores")
def listar(
    texto: str | None = Query(None, description="Busca por nombre, documento o contacto"),
    tipo_proveedor: TipoProveedor | None = None,
    tipo_residuo: TipoResiduo | None = None,
    municipio: str | None = None,
    activo: Literal["S", "N"] | None = None,
    _: dict = Depends(usuario_actual),
):
    return proveedores_service.listar(texto, tipo_proveedor, tipo_residuo, municipio, activo)


@router.get("/{id_proveedor}", response_model=ProveedorRespuesta, summary="Consultar un proveedor")
def obtener(id_proveedor: int, _: dict = Depends(usuario_actual)):
    return proveedores_service.obtener(id_proveedor)


@router.post("", response_model=ProveedorRespuesta, status_code=status.HTTP_201_CREATED, summary="Registrar proveedor")
def crear(datos: ProveedorEntrada, _: dict = Depends(solo_administrador)):
    return proveedores_service.crear(datos)


@router.put("/{id_proveedor}", response_model=ProveedorRespuesta, summary="Actualizar proveedor")
def actualizar(id_proveedor: int, datos: ProveedorEntrada, _: dict = Depends(solo_administrador)):
    return proveedores_service.actualizar(id_proveedor, datos)


@router.delete("/{id_proveedor}", response_model=Mensaje, summary="Eliminar proveedor")
def eliminar(id_proveedor: int, _: dict = Depends(solo_administrador)):
    proveedores_service.eliminar(id_proveedor)
    return {"mensaje": "Proveedor eliminado correctamente"}

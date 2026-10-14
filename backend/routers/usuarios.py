from typing import Literal

from fastapi import APIRouter, Depends, Query, status

from routers.dependencias import RESPUESTAS_COMUNES, solo_administrador
from schemas.base import Mensaje
from schemas.usuario import RolActualizar, RolRespuesta, UsuarioActualizar, UsuarioCrear, UsuarioRespuesta
from services import usuarios_service

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"], responses=RESPUESTAS_COMUNES)
router_roles = APIRouter(prefix="/api/roles", tags=["Usuarios"], responses=RESPUESTAS_COMUNES)


@router_roles.get("", response_model=list[RolRespuesta], summary="Listar roles")
def listar_roles(_: dict = Depends(solo_administrador)):
    return usuarios_service.listar_roles()


@router_roles.get("/{id_rol}", response_model=RolRespuesta, summary="Consultar un rol")
def obtener_rol(id_rol: int, _: dict = Depends(solo_administrador)):
    return usuarios_service.obtener_rol(id_rol)


@router_roles.put("/{id_rol}", response_model=RolRespuesta, summary="Editar nombre y descripción de un rol")
def actualizar_rol(id_rol: int, datos: RolActualizar, _: dict = Depends(solo_administrador)):
    """Cambia el nombre visible y la descripción. El código interno (ADMINISTRADOR / RECOLECTOR)
    no se modifica, porque es el que usan los permisos: así renombrar un rol nunca quita accesos."""
    return usuarios_service.actualizar_rol(id_rol, datos)


@router.get("", response_model=list[UsuarioRespuesta], summary="Listar y buscar usuarios")
def listar(
    texto: str | None = Query(None, description="Busca por nombre o correo"),
    id_rol: int | None = None,
    activo: Literal["S", "N"] | None = None,
    _: dict = Depends(solo_administrador),
):
    return usuarios_service.listar(texto, id_rol, activo)


@router.get("/{id_usuario}", response_model=UsuarioRespuesta, summary="Consultar un usuario")
def obtener(id_usuario: int, _: dict = Depends(solo_administrador)):
    return usuarios_service.obtener(id_usuario)


@router.post("", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED, summary="Crear usuario")
def crear(datos: UsuarioCrear, _: dict = Depends(solo_administrador)):
    return usuarios_service.crear(datos)


@router.put("/{id_usuario}", response_model=UsuarioRespuesta, summary="Actualizar usuario")
def actualizar(id_usuario: int, datos: UsuarioActualizar, usuario: dict = Depends(solo_administrador)):
    return usuarios_service.actualizar(id_usuario, datos, usuario)


@router.delete("/{id_usuario}", response_model=Mensaje, summary="Eliminar usuario")
def eliminar(id_usuario: int, usuario: dict = Depends(solo_administrador)):
    usuarios_service.eliminar(id_usuario, usuario)
    return {"mensaje": "Usuario eliminado correctamente"}

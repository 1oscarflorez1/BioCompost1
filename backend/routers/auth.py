from fastapi import APIRouter, Depends

from routers.dependencias import usuario_actual
from schemas.auth import LoginEntrada, TokenRespuesta, UsuarioSesion
from services import auth_service

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post(
    "/login",
    response_model=TokenRespuesta,
    summary="Iniciar sesión",
    responses={401: {"description": "Correo o contraseña incorrectos"}, 403: {"description": "Usuario inactivo"}},
)
def login(datos: LoginEntrada):
    """Valida las credenciales y devuelve un token JWT.

    En Swagger: copie el `access_token`, pulse **Authorize** y péguelo.
    """
    return auth_service.iniciar_sesion(datos.correo, datos.contrasena)


@router.get("/me", response_model=UsuarioSesion, summary="Usuario de la sesión actual")
def usuario_sesion(usuario: dict = Depends(usuario_actual)):
    return usuario

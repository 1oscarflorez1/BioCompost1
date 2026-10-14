from core.errores import NoAutorizado, Prohibido
from core.security import crear_token, verificar_contrasena
from database.connection import consultar_uno

# rol = código interno fijo (permisos); rol_nombre = nombre visible editable
SQL_USUARIO = """
    SELECT u.id_usuario, u.nombre, u.correo, u.contrasena_hash, u.activo,
           r.codigo AS rol, r.nombre AS rol_nombre
      FROM usuarios u
      JOIN roles r ON r.id_rol = u.id_rol
"""


def iniciar_sesion(correo: str, contrasena: str) -> dict:
    usuario = consultar_uno(SQL_USUARIO + " WHERE LOWER(u.correo) = LOWER(:correo)", {"correo": correo})
    if not usuario or not verificar_contrasena(contrasena, usuario["contrasena_hash"]):
        raise NoAutorizado("Correo o contraseña incorrectos")
    if usuario["activo"] != "S":
        raise Prohibido("El usuario está inactivo. Contacte al administrador de planta")
    return {"access_token": crear_token(usuario), "token_type": "bearer", "usuario": usuario}


def obtener_usuario_sesion(id_usuario: int) -> dict | None:
    return consultar_uno(SQL_USUARIO + " WHERE u.id_usuario = :id", {"id": id_usuario})

from core.errores import NoEncontrado, ReglaNegocio
from core.security import cifrar_contrasena
from database.connection import clausula_where, consultar, consultar_uno, ejecutar, insertar
from models.catalogos import Rol
from schemas.usuario import RolActualizar, UsuarioActualizar, UsuarioCrear

SQL_BASE = """
    SELECT u.id_usuario, u.nombre, u.correo, u.telefono, u.id_rol,
           r.codigo AS rol, r.nombre AS rol_nombre, u.activo, u.fecha_creacion
      FROM usuarios u
      JOIN roles r ON r.id_rol = u.id_rol
"""


def listar(texto: str | None = None, id_rol: int | None = None, activo: str | None = None) -> list[dict]:
    condiciones, parametros = [], {}
    if texto:
        condiciones.append("(UPPER(u.nombre) LIKE :texto OR UPPER(u.correo) LIKE :texto)")
        parametros["texto"] = f"%{texto.upper()}%"
    if id_rol:
        condiciones.append("u.id_rol = :id_rol")
        parametros["id_rol"] = id_rol
    if activo:
        condiciones.append("u.activo = :activo")
        parametros["activo"] = activo
    return consultar(SQL_BASE + clausula_where(condiciones) + " ORDER BY u.nombre", parametros)


def obtener(id_usuario: int) -> dict:
    usuario = consultar_uno(SQL_BASE + " WHERE u.id_usuario = :id", {"id": id_usuario})
    if not usuario:
        raise NoEncontrado(f"No existe el usuario con id {id_usuario}")
    return usuario


def _validar_rol(id_rol: int):
    if not consultar_uno("SELECT id_rol FROM roles WHERE id_rol = :id", {"id": id_rol}):
        raise ReglaNegocio("El rol seleccionado no existe")


def crear(datos: UsuarioCrear) -> dict:
    _validar_rol(datos.id_rol)
    nuevo_id = insertar(
        """INSERT INTO usuarios (nombre, correo, contrasena_hash, telefono, id_rol, activo)
           VALUES (:nombre, :correo, :contrasena_hash, :telefono, :id_rol, :activo)""",
        {
            "nombre": datos.nombre,
            "correo": datos.correo.lower(),
            "contrasena_hash": cifrar_contrasena(datos.contrasena),
            "telefono": datos.telefono,
            "id_rol": datos.id_rol,
            "activo": datos.activo,
        },
        "id_usuario",
    )
    return obtener(nuevo_id)


def actualizar(id_usuario: int, datos: UsuarioActualizar, usuario_actual: dict) -> dict:
    obtener(id_usuario)
    _validar_rol(datos.id_rol)
    if id_usuario == usuario_actual["id_usuario"]:
        rol_nuevo = consultar_uno("SELECT codigo FROM roles WHERE id_rol = :id", {"id": datos.id_rol})["codigo"]
        if datos.activo != "S" or rol_nuevo != Rol.ADMINISTRADOR:
            raise ReglaNegocio("No puede desactivar su propio usuario ni quitarse el rol de administrador")

    parametros = {
        "id": id_usuario,
        "nombre": datos.nombre,
        "correo": datos.correo.lower(),
        "telefono": datos.telefono,
        "id_rol": datos.id_rol,
        "activo": datos.activo,
    }
    cambio_contrasena = ""
    if datos.contrasena:
        cambio_contrasena = ", contrasena_hash = :contrasena_hash"
        parametros["contrasena_hash"] = cifrar_contrasena(datos.contrasena)

    ejecutar(
        f"""UPDATE usuarios
               SET nombre = :nombre, correo = :correo, telefono = :telefono,
                   id_rol = :id_rol, activo = :activo {cambio_contrasena}
             WHERE id_usuario = :id""",
        parametros,
    )
    return obtener(id_usuario)


def eliminar(id_usuario: int, usuario_actual: dict):
    if id_usuario == usuario_actual["id_usuario"]:
        raise ReglaNegocio("No puede eliminar su propio usuario")
    if ejecutar("DELETE FROM usuarios WHERE id_usuario = :id", {"id": id_usuario}) == 0:
        raise NoEncontrado(f"No existe el usuario con id {id_usuario}")


# ---------------------------------------------------------------------------
# Roles: el código interno (ADMINISTRADOR / RECOLECTOR) es fijo porque los
# permisos dependen de él; el nombre visible y la descripción sí se editan.
# ---------------------------------------------------------------------------
SQL_ROLES = """
    SELECT r.id_rol, r.codigo, r.nombre, r.descripcion,
           (SELECT COUNT(*) FROM usuarios u WHERE u.id_rol = r.id_rol) AS total_usuarios
      FROM roles r
"""


def listar_roles() -> list[dict]:
    return consultar(SQL_ROLES + " ORDER BY r.id_rol")


def obtener_rol(id_rol: int) -> dict:
    rol = consultar_uno(SQL_ROLES + " WHERE r.id_rol = :id", {"id": id_rol})
    if not rol:
        raise NoEncontrado(f"No existe el rol con id {id_rol}")
    return rol


def actualizar_rol(id_rol: int, datos: RolActualizar) -> dict:
    obtener_rol(id_rol)
    ejecutar(
        "UPDATE roles SET nombre = :nombre, descripcion = :descripcion WHERE id_rol = :id",
        {"nombre": datos.nombre, "descripcion": datos.descripcion, "id": id_rol},
    )
    return obtener_rol(id_rol)

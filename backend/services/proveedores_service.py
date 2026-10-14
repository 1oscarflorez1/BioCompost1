from core.errores import NoEncontrado
from database.connection import clausula_where, consultar, consultar_uno, ejecutar, insertar
from schemas.proveedor import ProveedorEntrada

SQL_BASE = """
    SELECT p.id_proveedor, p.nombre, p.tipo_proveedor, p.documento, p.contacto, p.telefono,
           p.direccion, p.municipio, p.tipo_residuo, p.activo, p.fecha_registro,
           (SELECT COUNT(*) FROM recolecciones r
             WHERE r.id_proveedor = p.id_proveedor) AS num_recolecciones,
           (SELECT NVL(SUM(r.peso_kg), 0) FROM recolecciones r
             WHERE r.id_proveedor = p.id_proveedor AND r.clasificacion <> 'RECHAZADO') AS kg_aportados
      FROM proveedores p
"""


def listar(texto=None, tipo_proveedor=None, tipo_residuo=None, municipio=None, activo=None) -> list[dict]:
    condiciones, parametros = [], {}
    if texto:
        condiciones.append(
            "(UPPER(p.nombre) LIKE :texto OR p.documento LIKE :texto OR UPPER(p.contacto) LIKE :texto)"
        )
        parametros["texto"] = f"%{texto.upper()}%"
    if tipo_proveedor:
        condiciones.append("p.tipo_proveedor = :tipo_proveedor")
        parametros["tipo_proveedor"] = tipo_proveedor
    if tipo_residuo:
        condiciones.append("p.tipo_residuo = :tipo_residuo")
        parametros["tipo_residuo"] = tipo_residuo
    if municipio:
        condiciones.append("UPPER(p.municipio) LIKE :municipio")
        parametros["municipio"] = f"%{municipio.upper()}%"
    if activo:
        condiciones.append("p.activo = :activo")
        parametros["activo"] = activo
    return consultar(SQL_BASE + clausula_where(condiciones) + " ORDER BY p.nombre", parametros)


def obtener(id_proveedor: int) -> dict:
    proveedor = consultar_uno(SQL_BASE + " WHERE p.id_proveedor = :id", {"id": id_proveedor})
    if not proveedor:
        raise NoEncontrado(f"No existe el proveedor con id {id_proveedor}")
    return proveedor


def crear(datos: ProveedorEntrada) -> dict:
    nuevo_id = insertar(
        """INSERT INTO proveedores (nombre, tipo_proveedor, documento, contacto, telefono,
                                    direccion, municipio, tipo_residuo, activo)
           VALUES (:nombre, :tipo_proveedor, :documento, :contacto, :telefono,
                   :direccion, :municipio, :tipo_residuo, :activo)""",
        datos.model_dump(),
        "id_proveedor",
    )
    return obtener(nuevo_id)


def actualizar(id_proveedor: int, datos: ProveedorEntrada) -> dict:
    obtener(id_proveedor)
    ejecutar(
        """UPDATE proveedores
              SET nombre = :nombre, tipo_proveedor = :tipo_proveedor, documento = :documento,
                  contacto = :contacto, telefono = :telefono, direccion = :direccion,
                  municipio = :municipio, tipo_residuo = :tipo_residuo, activo = :activo
            WHERE id_proveedor = :id""",
        {**datos.model_dump(), "id": id_proveedor},
    )
    return obtener(id_proveedor)


def eliminar(id_proveedor: int):
    if ejecutar("DELETE FROM proveedores WHERE id_proveedor = :id", {"id": id_proveedor}) == 0:
        raise NoEncontrado(f"No existe el proveedor con id {id_proveedor}")

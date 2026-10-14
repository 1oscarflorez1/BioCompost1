from core.errores import NoEncontrado, Prohibido, ReglaNegocio
from database.connection import clausula_where, consultar, consultar_uno, ejecutar, insertar
from models.catalogos import FasePila, Rol
from schemas.recoleccion import RecoleccionEntrada

SQL_BASE = """
    SELECT r.id_recoleccion, r.id_proveedor, p.nombre AS proveedor, p.municipio,
           r.id_usuario, u.nombre AS recolector, r.id_pila, pc.codigo AS pila,
           r.fecha_recoleccion, r.peso_kg, r.tipo_residuo, r.clasificacion,
           r.observaciones, r.fecha_registro
      FROM recolecciones r
      JOIN proveedores p ON p.id_proveedor = r.id_proveedor
      JOIN usuarios u    ON u.id_usuario   = r.id_usuario
      LEFT JOIN pilas_compost pc ON pc.id_pila = r.id_pila
"""


def listar(texto=None, fecha_desde=None, fecha_hasta=None, id_proveedor=None, id_pila=None,
           tipo_residuo=None, clasificacion=None, sin_pila=False, limite=None) -> list[dict]:
    condiciones, parametros = [], {}
    if texto:
        condiciones.append("(UPPER(p.nombre) LIKE :texto OR UPPER(p.municipio) LIKE :texto)")
        parametros["texto"] = f"%{texto.upper()}%"
    if fecha_desde:
        condiciones.append("r.fecha_recoleccion >= :fecha_desde")
        parametros["fecha_desde"] = fecha_desde
    if fecha_hasta:
        condiciones.append("r.fecha_recoleccion <= :fecha_hasta")
        parametros["fecha_hasta"] = fecha_hasta
    if id_proveedor:
        condiciones.append("r.id_proveedor = :id_proveedor")
        parametros["id_proveedor"] = id_proveedor
    if id_pila:
        condiciones.append("r.id_pila = :id_pila")
        parametros["id_pila"] = id_pila
    if sin_pila:
        condiciones.append("r.id_pila IS NULL AND r.clasificacion <> 'RECHAZADO'")
    if tipo_residuo:
        condiciones.append("r.tipo_residuo = :tipo_residuo")
        parametros["tipo_residuo"] = tipo_residuo
    if clasificacion:
        condiciones.append("r.clasificacion = :clasificacion")
        parametros["clasificacion"] = clasificacion
    sql = SQL_BASE + clausula_where(condiciones) + " ORDER BY r.fecha_recoleccion DESC, r.id_recoleccion DESC"
    if limite:
        sql += " FETCH FIRST :limite ROWS ONLY"
        parametros["limite"] = limite
    return consultar(sql, parametros)


def obtener(id_recoleccion: int) -> dict:
    recoleccion = consultar_uno(SQL_BASE + " WHERE r.id_recoleccion = :id", {"id": id_recoleccion})
    if not recoleccion:
        raise NoEncontrado(f"No existe la recolección con id {id_recoleccion}")
    return recoleccion


def _validar_proveedor(id_proveedor: int, id_actual: int | None = None):
    proveedor = consultar_uno("SELECT activo FROM proveedores WHERE id_proveedor = :id", {"id": id_proveedor})
    if not proveedor:
        raise ReglaNegocio("El proveedor seleccionado no existe")
    if proveedor["activo"] != "S" and id_proveedor != id_actual:
        raise ReglaNegocio("El proveedor seleccionado está inactivo")


def _validar_pila(id_pila: int | None, id_actual: int | None = None):
    if id_pila is None or id_pila == id_actual:
        return
    pila = consultar_uno("SELECT fase FROM pilas_compost WHERE id_pila = :id", {"id": id_pila})
    if not pila:
        raise ReglaNegocio("La pila seleccionada no existe")
    if pila["fase"] == FasePila.FINALIZADA:
        raise ReglaNegocio("No se puede asignar residuo a una pila FINALIZADA")


def _parametros(datos: RecoleccionEntrada) -> dict:
    parametros = datos.model_dump()
    parametros["peso_kg"] = round(datos.peso_kg, 2)
    return parametros


def crear(datos: RecoleccionEntrada, usuario: dict) -> dict:
    _validar_proveedor(datos.id_proveedor)
    _validar_pila(datos.id_pila)
    nuevo_id = insertar(
        """INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion,
                                      peso_kg, tipo_residuo, clasificacion, observaciones)
           VALUES (:id_proveedor, :id_usuario, :id_pila, :fecha_recoleccion,
                   :peso_kg, :tipo_residuo, :clasificacion, :observaciones)""",
        {**_parametros(datos), "id_usuario": usuario["id_usuario"]},
        "id_recoleccion",
    )
    return obtener(nuevo_id)


def actualizar(id_recoleccion: int, datos: RecoleccionEntrada, usuario: dict) -> dict:
    actual = obtener(id_recoleccion)
    if usuario["rol"] == Rol.RECOLECTOR and actual["id_usuario"] != usuario["id_usuario"]:
        raise Prohibido("Solo puede modificar las recolecciones que usted registró")
    _validar_proveedor(datos.id_proveedor, actual["id_proveedor"])
    _validar_pila(datos.id_pila, actual["id_pila"])
    ejecutar(
        """UPDATE recolecciones
              SET id_proveedor = :id_proveedor, id_pila = :id_pila,
                  fecha_recoleccion = :fecha_recoleccion, peso_kg = :peso_kg,
                  tipo_residuo = :tipo_residuo, clasificacion = :clasificacion,
                  observaciones = :observaciones
            WHERE id_recoleccion = :id""",
        {**_parametros(datos), "id": id_recoleccion},
    )
    return obtener(id_recoleccion)


def eliminar(id_recoleccion: int):
    if ejecutar("DELETE FROM recolecciones WHERE id_recoleccion = :id", {"id": id_recoleccion}) == 0:
        raise NoEncontrado(f"No existe la recolección con id {id_recoleccion}")

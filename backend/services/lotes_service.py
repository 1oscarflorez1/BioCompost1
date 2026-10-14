from core.errores import NoEncontrado, ReglaNegocio
from database.connection import clausula_where, consultar, consultar_uno, ejecutar, insertar
from models.catalogos import FasePila
from schemas.lote import LoteEntrada
from services import pilas_service

SQL_BASE = """
    SELECT l.id_lote, l.id_pila, p.codigo AS pila, l.codigo_lote, l.fecha_produccion,
           l.kilos_producidos, l.calidad, l.estado, l.observaciones
      FROM lotes_abono l
      JOIN pilas_compost p ON p.id_pila = l.id_pila
"""


def listar(texto=None, estado=None, calidad=None, id_pila=None) -> list[dict]:
    condiciones, parametros = [], {}
    if texto:
        condiciones.append("(UPPER(l.codigo_lote) LIKE :texto OR UPPER(p.codigo) LIKE :texto)")
        parametros["texto"] = f"%{texto.upper()}%"
    if estado:
        condiciones.append("l.estado = :estado")
        parametros["estado"] = estado
    if calidad:
        condiciones.append("l.calidad = :calidad")
        parametros["calidad"] = calidad
    if id_pila:
        condiciones.append("l.id_pila = :id_pila")
        parametros["id_pila"] = id_pila
    sql = SQL_BASE + clausula_where(condiciones) + " ORDER BY l.fecha_produccion DESC, l.codigo_lote DESC"
    return consultar(sql, parametros)


def obtener(id_lote: int) -> dict:
    lote = consultar_uno(SQL_BASE + " WHERE l.id_lote = :id", {"id": id_lote})
    if not lote:
        raise NoEncontrado(f"No existe el lote con id {id_lote}")
    return lote


def _validar(datos: LoteEntrada, id_lote: int | None = None):
    pila = pilas_service.resumen(datos.id_pila)
    if not pila:
        raise ReglaNegocio("La pila seleccionada no existe")
    if pila["fase"] not in (FasePila.MADURACION, FasePila.FINALIZADA):
        raise ReglaNegocio("Solo se pueden registrar lotes de pilas en fase MADURACION o FINALIZADA")
    if datos.fecha_produccion < pila["fecha_inicio"].date():
        raise ReglaNegocio("La fecha de producción es anterior al inicio de la pila")

    # El abono producido no puede superar el residuo que ingresó a la pila
    otros_lotes = consultar_uno(
        "SELECT NVL(SUM(kilos_producidos), 0) AS kg FROM lotes_abono WHERE id_pila = :id_pila AND id_lote <> :id_lote",
        {"id_pila": datos.id_pila, "id_lote": id_lote or 0},
    )["kg"]
    if otros_lotes + datos.kilos_producidos > pila["kg_recibidos"]:
        raise ReglaNegocio(
            f"El abono total de la pila ({otros_lotes + datos.kilos_producidos:,.0f} kg) supera el residuo "
            f"que recibió ({pila['kg_recibidos']:,.0f} kg)"
        )


def crear(datos: LoteEntrada) -> dict:
    _validar(datos)
    nuevo_id = insertar(
        """INSERT INTO lotes_abono (id_pila, codigo_lote, fecha_produccion, kilos_producidos, calidad, estado, observaciones)
           VALUES (:id_pila, :codigo_lote, :fecha_produccion, :kilos_producidos, :calidad, :estado, :observaciones)""",
        datos.model_dump(),
        "id_lote",
    )
    return obtener(nuevo_id)


def actualizar(id_lote: int, datos: LoteEntrada) -> dict:
    obtener(id_lote)
    _validar(datos, id_lote)
    ejecutar(
        """UPDATE lotes_abono
              SET id_pila = :id_pila, codigo_lote = :codigo_lote, fecha_produccion = :fecha_produccion,
                  kilos_producidos = :kilos_producidos, calidad = :calidad, estado = :estado,
                  observaciones = :observaciones
            WHERE id_lote = :id""",
        {**datos.model_dump(), "id": id_lote},
    )
    return obtener(id_lote)


def eliminar(id_lote: int):
    if ejecutar("DELETE FROM lotes_abono WHERE id_lote = :id", {"id": id_lote}) == 0:
        raise NoEncontrado(f"No existe el lote con id {id_lote}")


def trazabilidad(id_lote: int) -> dict:
    """Recorrido completo: lote -> pila -> recolecciones -> proveedores de origen."""
    lote = obtener(id_lote)
    recolecciones = consultar(
        """SELECT r.id_recoleccion, r.fecha_recoleccion, pr.nombre AS proveedor, pr.municipio,
                  pr.tipo_proveedor, r.tipo_residuo, r.peso_kg, r.clasificacion
             FROM recolecciones r
             JOIN proveedores pr ON pr.id_proveedor = r.id_proveedor
            WHERE r.id_pila = :id_pila
            ORDER BY r.fecha_recoleccion""",
        {"id_pila": lote["id_pila"]},
    )
    kg_residuo = sum(r["peso_kg"] for r in recolecciones)
    abono_pila = consultar_uno(
        "SELECT SUM(kilos_producidos) AS kg FROM lotes_abono WHERE id_pila = :id", {"id": lote["id_pila"]}
    )["kg"]
    return {
        "lote": lote,
        "kg_residuo_pila": kg_residuo,
        "kg_abono_pila": abono_pila,
        "rendimiento_pct": round(abono_pila / kg_residuo * 100, 1) if kg_residuo else None,
        "num_proveedores": len({r["proveedor"] for r in recolecciones}),
        "recolecciones": recolecciones,
    }

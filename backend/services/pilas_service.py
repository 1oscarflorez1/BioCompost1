from core.errores import NoEncontrado
from database.connection import clausula_where, consultar, consultar_uno, ejecutar, insertar
from models.catalogos import FasePila
from schemas.pila import PilaEntrada
from services.monitoreos_service import evaluar_alerta

# Cada pila con: kilos recibidos, abono producido y su última medición
SQL_BASE = """
    SELECT p.id_pila, p.codigo, p.ubicacion, p.fecha_inicio, p.fecha_fin, p.fase,
           p.capacidad_kg, p.observaciones,
           NVL(r.kg_recibidos, 0)      AS kg_recibidos,
           NVL(r.num_recolecciones, 0) AS num_recolecciones,
           NVL(l.kg_abono, 0)          AS kg_abono,
           TRUNC(NVL(p.fecha_fin, SYSDATE) - p.fecha_inicio) AS dias_proceso,
           m.fecha_monitoreo AS ultimo_monitoreo,
           m.temperatura     AS ultima_temperatura,
           m.humedad         AS ultima_humedad
      FROM pilas_compost p
      LEFT JOIN (SELECT id_pila, SUM(peso_kg) AS kg_recibidos, COUNT(*) AS num_recolecciones
                   FROM recolecciones GROUP BY id_pila) r ON r.id_pila = p.id_pila
      LEFT JOIN (SELECT id_pila, SUM(kilos_producidos) AS kg_abono
                   FROM lotes_abono GROUP BY id_pila) l ON l.id_pila = p.id_pila
      LEFT JOIN (SELECT id_pila, fecha_monitoreo, temperatura, humedad,
                        ROW_NUMBER() OVER (PARTITION BY id_pila
                                           ORDER BY fecha_monitoreo DESC, id_monitoreo DESC) AS fila
                   FROM monitoreo_pilas) m ON m.id_pila = p.id_pila AND m.fila = 1
"""


def _con_alerta(pila: dict) -> dict:
    activa = pila["fase"] != FasePila.FINALIZADA
    pila["alerta"] = evaluar_alerta(pila["ultima_temperatura"], pila["ultima_humedad"]) if activa else None
    return pila


def listar(fase=None, texto=None, solo_activas=False) -> list[dict]:
    condiciones, parametros = [], {}
    if fase:
        condiciones.append("p.fase = :fase")
        parametros["fase"] = fase
    if solo_activas:
        condiciones.append("p.fase <> 'FINALIZADA'")
    if texto:
        condiciones.append("(UPPER(p.codigo) LIKE :texto OR UPPER(p.ubicacion) LIKE :texto)")
        parametros["texto"] = f"%{texto.upper()}%"
    sql = SQL_BASE + clausula_where(condiciones) + " ORDER BY p.fecha_inicio DESC"
    return [_con_alerta(pila) for pila in consultar(sql, parametros)]


def obtener(id_pila: int) -> dict:
    pila = consultar_uno(SQL_BASE + " WHERE p.id_pila = :id", {"id": id_pila})
    if not pila:
        raise NoEncontrado(f"No existe la pila con id {id_pila}")
    return _con_alerta(pila)


def crear(datos: PilaEntrada) -> dict:
    nuevo_id = insertar(
        """INSERT INTO pilas_compost (codigo, ubicacion, fecha_inicio, fecha_fin, fase, capacidad_kg, observaciones)
           VALUES (:codigo, :ubicacion, :fecha_inicio, :fecha_fin, :fase, :capacidad_kg, :observaciones)""",
        datos.model_dump(),
        "id_pila",
    )
    return obtener(nuevo_id)


def actualizar(id_pila: int, datos: PilaEntrada) -> dict:
    obtener(id_pila)
    ejecutar(
        """UPDATE pilas_compost
              SET codigo = :codigo, ubicacion = :ubicacion, fecha_inicio = :fecha_inicio,
                  fecha_fin = :fecha_fin, fase = :fase, capacidad_kg = :capacidad_kg,
                  observaciones = :observaciones
            WHERE id_pila = :id""",
        {**datos.model_dump(), "id": id_pila},
    )
    return obtener(id_pila)


def eliminar(id_pila: int):
    if ejecutar("DELETE FROM pilas_compost WHERE id_pila = :id", {"id": id_pila}) == 0:
        raise NoEncontrado(f"No existe la pila con id {id_pila}")


def contar_por_fase() -> list[dict]:
    return consultar("SELECT fase, COUNT(*) AS cantidad FROM pilas_compost GROUP BY fase")


def resumen(id_pila: int) -> dict | None:
    """Datos mínimos de una pila para validaciones de otros módulos."""
    return consultar_uno(
        """SELECT p.id_pila, p.codigo, p.fase, p.fecha_inicio,
                  (SELECT NVL(SUM(r.peso_kg), 0) FROM recolecciones r WHERE r.id_pila = p.id_pila) AS kg_recibidos
             FROM pilas_compost p
            WHERE p.id_pila = :id""",
        {"id": id_pila},
    )

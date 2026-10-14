from core.errores import NoEncontrado, ReglaNegocio
from database.connection import clausula_where, consultar, consultar_uno, ejecutar, insertar
from models.catalogos import HUMEDAD_MAXIMA, HUMEDAD_MINIMA, TEMPERATURA_MAXIMA, FasePila
from schemas.monitoreo import MonitoreoEntrada

SQL_BASE = """
    SELECT m.id_monitoreo, m.id_pila, p.codigo AS pila, p.fase, m.id_usuario, u.nombre AS usuario,
           m.fecha_monitoreo, m.temperatura, m.humedad, m.ph, m.volteo, m.observaciones
      FROM monitoreo_pilas m
      JOIN pilas_compost p ON p.id_pila = m.id_pila
      JOIN usuarios u      ON u.id_usuario = m.id_usuario
"""


def evaluar_alerta(temperatura: float | None, humedad: float | None) -> str | None:
    """Devuelve un texto de alerta si la medición está fuera de los rangos recomendados."""
    alertas = []
    if temperatura is not None and temperatura > TEMPERATURA_MAXIMA:
        alertas.append(f"Temperatura alta ({temperatura} °C)")
    if humedad is not None and humedad < HUMEDAD_MINIMA:
        alertas.append(f"Humedad baja ({humedad} %)")
    if humedad is not None and humedad > HUMEDAD_MAXIMA:
        alertas.append(f"Humedad alta ({humedad} %)")
    return ", ".join(alertas) or None


def _con_alerta(fila: dict) -> dict:
    fila["alerta"] = evaluar_alerta(fila["temperatura"], fila["humedad"])
    return fila


def listar(id_pila=None, fecha_desde=None, fecha_hasta=None, solo_alertas=False) -> list[dict]:
    condiciones, parametros = [], {}
    if id_pila:
        condiciones.append("m.id_pila = :id_pila")
        parametros["id_pila"] = id_pila
    if fecha_desde:
        condiciones.append("m.fecha_monitoreo >= :fecha_desde")
        parametros["fecha_desde"] = fecha_desde
    if fecha_hasta:
        condiciones.append("m.fecha_monitoreo <= :fecha_hasta")
        parametros["fecha_hasta"] = fecha_hasta
    if solo_alertas:
        condiciones.append("(m.temperatura > :tmax OR m.humedad < :hmin OR m.humedad > :hmax)")
        parametros.update(tmax=TEMPERATURA_MAXIMA, hmin=HUMEDAD_MINIMA, hmax=HUMEDAD_MAXIMA)
    sql = SQL_BASE + clausula_where(condiciones) + " ORDER BY m.fecha_monitoreo DESC, m.id_monitoreo DESC"
    return [_con_alerta(fila) for fila in consultar(sql, parametros)]


def obtener(id_monitoreo: int) -> dict:
    monitoreo = consultar_uno(SQL_BASE + " WHERE m.id_monitoreo = :id", {"id": id_monitoreo})
    if not monitoreo:
        raise NoEncontrado(f"No existe el monitoreo con id {id_monitoreo}")
    return _con_alerta(monitoreo)


def _validar_pila(datos: MonitoreoEntrada, id_pila_actual: int | None = None):
    pila = consultar_uno(
        "SELECT fase, fecha_inicio FROM pilas_compost WHERE id_pila = :id", {"id": datos.id_pila}
    )
    if not pila:
        raise ReglaNegocio("La pila seleccionada no existe")
    if pila["fase"] == FasePila.FINALIZADA and datos.id_pila != id_pila_actual:
        raise ReglaNegocio("No se pueden registrar monitoreos en una pila FINALIZADA")
    if datos.fecha_monitoreo < pila["fecha_inicio"].date():
        raise ReglaNegocio("La fecha del monitoreo es anterior a la fecha de inicio de la pila")


def crear(datos: MonitoreoEntrada, usuario: dict) -> dict:
    _validar_pila(datos)
    nuevo_id = insertar(
        """INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura,
                                        humedad, ph, volteo, observaciones)
           VALUES (:id_pila, :id_usuario, :fecha_monitoreo, :temperatura,
                   :humedad, :ph, :volteo, :observaciones)""",
        {**datos.model_dump(), "id_usuario": usuario["id_usuario"]},
        "id_monitoreo",
    )
    return obtener(nuevo_id)


def actualizar(id_monitoreo: int, datos: MonitoreoEntrada) -> dict:
    actual = obtener(id_monitoreo)
    _validar_pila(datos, actual["id_pila"])
    ejecutar(
        """UPDATE monitoreo_pilas
              SET id_pila = :id_pila, fecha_monitoreo = :fecha_monitoreo, temperatura = :temperatura,
                  humedad = :humedad, ph = :ph, volteo = :volteo, observaciones = :observaciones
            WHERE id_monitoreo = :id""",
        {**datos.model_dump(), "id": id_monitoreo},
    )
    return obtener(id_monitoreo)


def eliminar(id_monitoreo: int):
    if ejecutar("DELETE FROM monitoreo_pilas WHERE id_monitoreo = :id", {"id": id_monitoreo}) == 0:
        raise NoEncontrado(f"No existe el monitoreo con id {id_monitoreo}")

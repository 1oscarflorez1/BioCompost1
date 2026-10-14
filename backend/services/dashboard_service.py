from datetime import date

from database.connection import consultar, consultar_uno
from models.catalogos import FasePila
from services import pilas_service, recolecciones_service, reportes_service

SQL_INDICADORES = """
    SELECT
      (SELECT NVL(SUM(peso_kg), 0) FROM recolecciones WHERE clasificacion <> 'RECHAZADO') AS kg_desviados,
      (SELECT NVL(SUM(kilos_producidos), 0) FROM lotes_abono)                            AS kg_abono_producido,
      (SELECT NVL(SUM(kilos_producidos), 0) FROM lotes_abono WHERE estado = 'DISPONIBLE') AS kg_abono_disponible,
      (SELECT COUNT(*) FROM proveedores   WHERE activo = 'S')                              AS proveedores_activos,
      (SELECT COUNT(*) FROM pilas_compost WHERE fase <> 'FINALIZADA')                      AS pilas_activas,
      (SELECT COUNT(*) FROM recolecciones
        WHERE fecha_recoleccion >= TRUNC(SYSDATE, 'MM'))                                   AS recolecciones_mes,
      (SELECT NVL(SUM(peso_kg), 0) FROM recolecciones
        WHERE fecha_recoleccion >= TRUNC(SYSDATE, 'MM') AND clasificacion <> 'RECHAZADO')  AS kg_mes
      FROM dual
"""

# Rendimiento: abono producido / residuo que ingresó a las pilas ya finalizadas
SQL_CONVERSION = """
    SELECT ROUND((SELECT NVL(SUM(kilos_producidos), 0) FROM lotes_abono) /
                 NULLIF((SELECT SUM(r.peso_kg)
                           FROM recolecciones r
                           JOIN pilas_compost p ON p.id_pila = r.id_pila
                          WHERE p.fase = 'FINALIZADA'), 0) * 100, 1) AS tasa
      FROM dual
"""

SQL_POR_TIPO = """
    SELECT tipo_residuo, ROUND(SUM(peso_kg) / 1000, 2) AS toneladas
      FROM recolecciones
     WHERE clasificacion <> 'RECHAZADO'
     GROUP BY tipo_residuo
     ORDER BY toneladas DESC
"""


def _ultimos_meses(cantidad: int) -> list[str]:
    hoy = date.today()
    meses = []
    for i in range(cantidad - 1, -1, -1):
        anio, mes = hoy.year, hoy.month - i
        while mes <= 0:
            mes += 12
            anio -= 1
        meses.append(f"{anio}-{mes:02d}")
    return meses


def obtener() -> dict:
    indicadores = consultar_uno(SQL_INDICADORES)
    indicadores["toneladas_desviadas"] = round(indicadores.pop("kg_desviados") / 1000, 2)
    indicadores["tasa_conversion_pct"] = consultar_uno(SQL_CONVERSION)["tasa"]

    # Últimos 6 meses (se completan con ceros los meses sin movimiento)
    meses = _ultimos_meses(6)
    anio_ini, mes_ini = map(int, meses[0].split("-"))
    datos_mes = {m["mes"]: m for m in reportes_service.mensual_entre(date(anio_ini, mes_ini, 1), date.today())}
    por_mes = [
        {
            "mes": mes,
            "toneladas_desviadas": datos_mes.get(mes, {}).get("toneladas_desviadas", 0),
            "kg_abono_producido": datos_mes.get(mes, {}).get("kg_abono_producido", 0),
        }
        for mes in meses
    ]

    cantidad_fase = {f["fase"]: f["cantidad"] for f in pilas_service.contar_por_fase()}
    pilas_por_fase = [{"fase": fase.value, "cantidad": cantidad_fase.get(fase.value, 0)} for fase in FasePila]

    alertas = [
        {
            "id_pila": p["id_pila"],
            "codigo": p["codigo"],
            "fase": p["fase"],
            "fecha": p["ultimo_monitoreo"],
            "alerta": p["alerta"],
        }
        for p in pilas_service.listar(solo_activas=True)
        if p["alerta"]
    ]

    return {
        "indicadores": indicadores,
        "por_mes": por_mes,
        "por_tipo": consultar(SQL_POR_TIPO),
        "pilas_por_fase": pilas_por_fase,
        "alertas": alertas,
        "ultimas_recolecciones": recolecciones_service.listar(limite=5),
    }

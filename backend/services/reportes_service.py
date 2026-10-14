from datetime import date

from database.connection import consultar

# Consolidado mensual: residuo desviado del vertedero vs. abono producido
SQL_MENSUAL = """
    WITH entradas AS (
      SELECT TRUNC(fecha_recoleccion, 'MM') AS mes,
             COUNT(*) AS num_recolecciones,
             SUM(CASE WHEN clasificacion <> 'RECHAZADO' THEN peso_kg ELSE 0 END) AS kg_desviados,
             SUM(CASE WHEN clasificacion  = 'RECHAZADO' THEN peso_kg ELSE 0 END) AS kg_rechazados
        FROM recolecciones
       GROUP BY TRUNC(fecha_recoleccion, 'MM')
    ), produccion AS (
      SELECT TRUNC(fecha_produccion, 'MM') AS mes,
             COUNT(*) AS num_lotes,
             SUM(kilos_producidos) AS kg_abono
        FROM lotes_abono
       GROUP BY TRUNC(fecha_produccion, 'MM')
    )
    SELECT TO_CHAR(NVL(e.mes, p.mes), 'YYYY-MM')    AS mes,
           NVL(e.num_recolecciones, 0)              AS num_recolecciones,
           NVL(e.kg_desviados, 0)                   AS kg_desviados,
           NVL(e.kg_rechazados, 0)                  AS kg_rechazados,
           ROUND(NVL(e.kg_desviados, 0) / 1000, 2)  AS toneladas_desviadas,
           ROUND(NVL(e.kg_rechazados, 0) / 1000, 2) AS toneladas_rechazadas,
           NVL(p.num_lotes, 0)                      AS num_lotes,
           NVL(p.kg_abono, 0)                       AS kg_abono_producido
      FROM entradas e
      FULL OUTER JOIN produccion p ON p.mes = e.mes
     WHERE NVL(e.mes, p.mes) BETWEEN :desde AND :hasta
     ORDER BY 1
"""

SQL_POR_PROVEEDOR = """
    SELECT pr.id_proveedor, pr.nombre AS proveedor, pr.tipo_proveedor, pr.municipio,
           COUNT(r.id_recoleccion) AS num_recolecciones,
           NVL(SUM(CASE WHEN r.clasificacion <> 'RECHAZADO' THEN r.peso_kg END), 0) AS kg_aprovechados,
           NVL(SUM(CASE WHEN r.clasificacion  = 'RECHAZADO' THEN r.peso_kg END), 0) AS kg_rechazados
      FROM proveedores pr
      LEFT JOIN recolecciones r
             ON r.id_proveedor = pr.id_proveedor
            AND r.fecha_recoleccion BETWEEN :fecha_desde AND :fecha_hasta
     GROUP BY pr.id_proveedor, pr.nombre, pr.tipo_proveedor, pr.municipio
     ORDER BY kg_aprovechados DESC, pr.nombre
"""


def mensual_entre(desde: date, hasta: date) -> list[dict]:
    return consultar(SQL_MENSUAL, {"desde": desde, "hasta": hasta})


def consolidado_mensual(anio: int) -> dict:
    meses = mensual_entre(date(anio, 1, 1), date(anio, 12, 1))
    # Los totales se calculan con los kilos exactos (no sumando meses ya redondeados)
    totales = {
        "num_recolecciones": sum(m["num_recolecciones"] for m in meses),
        "toneladas_desviadas": round(sum(m["kg_desviados"] for m in meses) / 1000, 2),
        "toneladas_rechazadas": round(sum(m["kg_rechazados"] for m in meses) / 1000, 2),
        "num_lotes": sum(m["num_lotes"] for m in meses),
        "kg_abono_producido": sum(m["kg_abono_producido"] for m in meses),
    }
    return {"anio": anio, "meses": meses, "totales": totales}


def por_proveedor(fecha_desde: date, fecha_hasta: date) -> list[dict]:
    return consultar(SQL_POR_PROVEEDOR, {"fecha_desde": fecha_desde, "fecha_hasta": fecha_hasta})


def anios_disponibles() -> list[int]:
    filas = consultar(
        """SELECT DISTINCT anio FROM (
               SELECT EXTRACT(YEAR FROM fecha_recoleccion) AS anio FROM recolecciones
               UNION
               SELECT EXTRACT(YEAR FROM fecha_produccion) FROM lotes_abono)
           ORDER BY anio DESC"""
    )
    return [int(f["anio"]) for f in filas] or [date.today().year]

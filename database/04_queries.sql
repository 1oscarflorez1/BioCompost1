-- =====================================================================
-- BioCompost - 04_queries.sql
-- Consultas SQL relevantes para el funcionamiento del sistema.
-- Son las mismas que ejecuta el backend (carpeta backend/services) con
-- variables de enlace (:variable). En SQL Developer se pueden ejecutar
-- y el programa pedirá el valor de cada variable.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. Autenticación: buscar el usuario por correo junto con su rol
-- ---------------------------------------------------------------------
SELECT u.id_usuario, u.nombre, u.correo, u.contrasena_hash, u.activo,
       r.id_rol, r.codigo AS rol, r.nombre AS rol_nombre
  FROM usuarios u
  JOIN roles r ON r.id_rol = u.id_rol
 WHERE LOWER(u.correo) = LOWER(:correo);

-- ---------------------------------------------------------------------
-- 2. Búsqueda de proveedores por texto, tipo y municipio (filtros)
-- ---------------------------------------------------------------------
SELECT id_proveedor, nombre, tipo_proveedor, documento, municipio, tipo_residuo, activo
  FROM proveedores
 WHERE (:texto IS NULL OR UPPER(nombre) LIKE '%' || UPPER(:texto) || '%'
                       OR documento LIKE '%' || :texto || '%')
   AND (:tipo_proveedor IS NULL OR tipo_proveedor = :tipo_proveedor)
   AND (:municipio IS NULL OR municipio = :municipio)
 ORDER BY nombre;

-- ---------------------------------------------------------------------
-- 3. Recolecciones con su origen, recolector y pila (filtro por fechas)
-- ---------------------------------------------------------------------
SELECT r.id_recoleccion, r.fecha_recoleccion, p.nombre AS proveedor, p.municipio,
       r.tipo_residuo, r.peso_kg, r.clasificacion, u.nombre AS recolector,
       pc.codigo AS pila
  FROM recolecciones r
  JOIN proveedores p     ON p.id_proveedor = r.id_proveedor
  JOIN usuarios u        ON u.id_usuario   = r.id_usuario
  LEFT JOIN pilas_compost pc ON pc.id_pila = r.id_pila
 WHERE r.fecha_recoleccion BETWEEN :fecha_desde AND :fecha_hasta
 ORDER BY r.fecha_recoleccion DESC;

-- ---------------------------------------------------------------------
-- 4. FILTRO REQUERIDO: pilas por fase de maduración, con los kilos
--    recibidos y la última medición registrada
-- ---------------------------------------------------------------------
SELECT pc.id_pila, pc.codigo, pc.fase, pc.fecha_inicio, pc.ubicacion,
       (SELECT NVL(SUM(r.peso_kg), 0)
          FROM recolecciones r
         WHERE r.id_pila = pc.id_pila)            AS kg_recibidos,
       (SELECT MAX(m.fecha_monitoreo)
          FROM monitoreo_pilas m
         WHERE m.id_pila = pc.id_pila)            AS ultimo_monitoreo
  FROM pilas_compost pc
 WHERE pc.fase = :fase
 ORDER BY pc.fecha_inicio DESC;

-- ---------------------------------------------------------------------
-- 5. REPORTE REQUERIDO: consolidado mensual de toneladas transformadas
--    (residuo desviado del vertedero vs. abono producido)
-- ---------------------------------------------------------------------
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
SELECT TO_CHAR(NVL(e.mes, p.mes), 'YYYY-MM')       AS mes,
       NVL(e.num_recolecciones, 0)                 AS num_recolecciones,
       ROUND(NVL(e.kg_desviados, 0) / 1000, 2)     AS toneladas_desviadas,
       ROUND(NVL(e.kg_rechazados, 0) / 1000, 2)    AS toneladas_rechazadas,
       NVL(p.num_lotes, 0)                         AS num_lotes,
       NVL(p.kg_abono, 0)                          AS kg_abono_producido
  FROM entradas e
  FULL OUTER JOIN produccion p ON p.mes = e.mes
 WHERE EXTRACT(YEAR FROM NVL(e.mes, p.mes)) = :anio
 ORDER BY 1;

-- ---------------------------------------------------------------------
-- 6. Indicadores del dashboard
-- ---------------------------------------------------------------------
SELECT
  (SELECT NVL(SUM(peso_kg), 0) FROM recolecciones WHERE clasificacion <> 'RECHAZADO') AS kg_desviados,
  (SELECT NVL(SUM(kilos_producidos), 0) FROM lotes_abono)                            AS kg_abono_producido,
  (SELECT COUNT(*) FROM proveedores   WHERE activo = 'S')                              AS proveedores_activos,
  (SELECT COUNT(*) FROM pilas_compost WHERE fase <> 'FINALIZADA')                      AS pilas_activas,
  (SELECT COUNT(*) FROM recolecciones
    WHERE fecha_recoleccion >= TRUNC(SYSDATE, 'MM'))                                   AS recolecciones_mes,
  (SELECT NVL(SUM(kilos_producidos), 0) FROM lotes_abono WHERE estado = 'DISPONIBLE')  AS kg_abono_disponible
  FROM dual;

-- Tasa de conversión: abono producido / residuo que ingresó a pilas ya finalizadas
SELECT ROUND(
         (SELECT NVL(SUM(l.kilos_producidos), 0) FROM lotes_abono l) /
         NULLIF((SELECT SUM(r.peso_kg)
                   FROM recolecciones r
                   JOIN pilas_compost p ON p.id_pila = r.id_pila
                  WHERE p.fase = 'FINALIZADA'), 0) * 100, 1) AS tasa_conversion_pct
  FROM dual;

-- Residuo recibido por tipo (gráfico de torta)
SELECT tipo_residuo, ROUND(SUM(peso_kg) / 1000, 2) AS toneladas
  FROM recolecciones
 WHERE clasificacion <> 'RECHAZADO'
 GROUP BY tipo_residuo
 ORDER BY toneladas DESC;

-- Cantidad de pilas por fase
SELECT fase, COUNT(*) AS cantidad
  FROM pilas_compost
 GROUP BY fase;

-- ---------------------------------------------------------------------
-- 7. Alertas: última medición de cada pila activa fuera de rango
--    (temperatura > 70 °C o humedad fuera de 40 % - 65 %)
-- ---------------------------------------------------------------------
SELECT p.codigo, p.fase, m.fecha_monitoreo, m.temperatura, m.humedad
  FROM pilas_compost p
  JOIN monitoreo_pilas m ON m.id_pila = p.id_pila
 WHERE p.fase <> 'FINALIZADA'
   AND m.fecha_monitoreo = (SELECT MAX(m2.fecha_monitoreo)
                              FROM monitoreo_pilas m2
                             WHERE m2.id_pila = p.id_pila)
   AND (m.temperatura > 70 OR m.humedad < 40 OR m.humedad > 65);

-- ---------------------------------------------------------------------
-- 8. Consolidado por proveedor en un rango de fechas
-- ---------------------------------------------------------------------
SELECT pr.nombre AS proveedor, pr.tipo_proveedor, pr.municipio,
       COUNT(r.id_recoleccion)                                                  AS num_recolecciones,
       NVL(SUM(CASE WHEN r.clasificacion <> 'RECHAZADO' THEN r.peso_kg END), 0) AS kg_aprovechados,
       NVL(SUM(CASE WHEN r.clasificacion  = 'RECHAZADO' THEN r.peso_kg END), 0) AS kg_rechazados
  FROM proveedores pr
  LEFT JOIN recolecciones r
         ON r.id_proveedor = pr.id_proveedor
        AND r.fecha_recoleccion BETWEEN :fecha_desde AND :fecha_hasta
 GROUP BY pr.nombre, pr.tipo_proveedor, pr.municipio
 ORDER BY kg_aprovechados DESC;

-- ---------------------------------------------------------------------
-- 9. Trazabilidad de un lote de abono: lote -> pila -> recolecciones -> proveedores
-- ---------------------------------------------------------------------
SELECT l.codigo_lote, l.kilos_producidos, p.codigo AS pila,
       r.fecha_recoleccion, pr.nombre AS proveedor, pr.municipio,
       r.tipo_residuo, r.peso_kg
  FROM lotes_abono l
  JOIN pilas_compost p   ON p.id_pila = l.id_pila
  JOIN recolecciones r   ON r.id_pila = p.id_pila
  JOIN proveedores pr    ON pr.id_proveedor = r.id_proveedor
 WHERE l.codigo_lote = :codigo_lote
 ORDER BY r.fecha_recoleccion;

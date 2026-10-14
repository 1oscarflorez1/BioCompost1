-- =====================================================================
-- BioCompost - consola.sql
-- Formato para ver las tablas cómodamente en SQL*Plus.
-- Lo ejecuta automáticamente consola_oracle.bat al conectarse.
-- =====================================================================
SET FEEDBACK OFF
ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD';
SET LINESIZE 200
SET PAGESIZE 60
SET TAB OFF
SET FEEDBACK ON
SET SQLPROMPT "BioCompost> "

COLUMN tabla            FORMAT A18
COLUMN nombre           FORMAT A30 TRUNCATED
COLUMN descripcion      FORMAT A45 TRUNCATED
COLUMN observaciones    FORMAT A30 TRUNCATED
COLUMN direccion        FORMAT A28 TRUNCATED
COLUMN contacto         FORMAT A18 TRUNCATED
COLUMN correo           FORMAT A32
COLUMN contrasena_hash  FORMAT A12 TRUNCATED
COLUMN municipio        FORMAT A11
COLUMN codigo           FORMAT A14
COLUMN codigo_lote      FORMAT A11
COLUMN ubicacion        FORMAT A16 TRUNCATED
COLUMN tipo_proveedor   FORMAT A14
COLUMN tipo_residuo     FORMAT A11
COLUMN clasificacion    FORMAT A13
COLUMN fase             FORMAT A13
COLUMN documento        FORMAT A12
COLUMN telefono         FORMAT A11
COLUMN calidad          FORMAT A10
COLUMN estado           FORMAT A11

PROMPT
PROMPT ============ Tablas del proyecto BioCompost (Oracle) ============
SELECT 'ROLES' AS tabla, COUNT(*) AS registros FROM roles
UNION ALL SELECT 'USUARIOS', COUNT(*) FROM usuarios
UNION ALL SELECT 'PROVEEDORES', COUNT(*) FROM proveedores
UNION ALL SELECT 'PILAS_COMPOST', COUNT(*) FROM pilas_compost
UNION ALL SELECT 'RECOLECCIONES', COUNT(*) FROM recolecciones
UNION ALL SELECT 'MONITOREO_PILAS', COUNT(*) FROM monitoreo_pilas
UNION ALL SELECT 'LOTES_ABONO', COUNT(*) FROM lotes_abono;

PROMPT Escriba una consulta, terminela con punto y coma y presione Enter. Ejemplos:
PROMPT   SELECT * FROM proveedores;        <- todas las columnas de una tabla
PROMPT   SELECT codigo, fase FROM pilas_compost WHERE fase = 'TERMOFILICA';   <- con filtro
PROMPT   DESC recolecciones                <- columnas y tipos de una tabla
PROMPT   EXIT                              <- salir
PROMPT

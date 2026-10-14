# BioCompost — Resumen del proyecto (documento fuente para NotebookLM)

## 1. Contexto y problema

En las zonas rurales y agrícolas del Valle del Cauca, las plazas de mercado, las fincas y las empresas
agroindustriales generan a diario grandes cantidades de residuos orgánicos: cáscaras y restos de frutas y
hortalizas, estiércol de ganado y cerdos, y bagazo de caña. La mayoría termina en rellenos sanitarios, donde se
descompone sin control, genera lixiviados y gases de efecto invernadero, y ocupa espacio en vertederos.

Esos mismos residuos pueden convertirse en **compost (abono orgánico)**, un insumo valioso para el campo. Sin
embargo, para que una planta de compostaje funcione bien necesita saber **cuánto residuo recibe, de dónde viene,
en qué estado llega, en qué pila se transforma, cómo avanza cada pila y cuánto abono produce**. Cuando esa
información se lleva en papel o en hojas de cálculo sueltas se pierde la trazabilidad y no es posible demostrar
el impacto ambiental.

## 2. Solución: BioCompost

BioCompost es una **aplicación web Full Stack** que gestiona la ruta de recolección de residuos orgánicos y
controla su transformación en abono, con trazabilidad completa:

**Proveedor → Recolección (pesaje) → Pila de compostaje → Monitoreo → Lote de abono**

De cualquier lote de abono se puede saber de qué pila salió, qué recolecciones la alimentaron y qué
proveedores aportaron el residuo.

### Usuarios (roles)
- **Administrador de planta:** gestiona todo el sistema: usuarios, roles, proveedores, pilas, mediciones y lotes.
- **Recolector / Proveedor:** registra las recolecciones en campo, edita solo las suyas y consulta la información.

Cada rol tiene un código interno fijo, que es el que usan los permisos, y un nombre visible que el administrador
puede editar junto con la descripción (por ejemplo, llamar al rol "Jefe de planta") sin que nadie pierda accesos.

### Los 5 módulos funcionales
1. **Autenticación y perfiles:** inicio de sesión con token JWT, dos roles con permisos distintos, gestión de
   usuarios (crear, editar, desactivar, eliminar) y edición del nombre y la descripción de los roles. Las
   contraseñas se guardan cifradas con bcrypt.
2. **Gestión de proveedores de residuos:** CRUD de puntos de recolección con su tipo (plaza de mercado, finca,
   agroindustria), ubicación, contacto y tipo de residuo principal (frutas, hortalizas, estiércol, bagazo, mixto).
   Búsqueda por nombre, NIT o contacto y filtros por tipo, residuo, municipio y estado.
3. **Registro de recolecciones y entradas:** control del pesaje en báscula, fecha, origen, tipo de residuo y
   clasificación (apto, condicionado o rechazado), y la pila a la que se destina. Filtros por fechas, proveedor,
   tipo, clasificación, pila y entradas pendientes de asignar.
4. **Control de pilas de compostaje:** cada pila avanza por las fases del compostaje: **mesofílica** (inicio,
   25–45 °C), **termofílica** (45–70 °C, se eliminan patógenos), **enfriamiento**, **maduración** y
   **finalizada**. Se registran mediciones de temperatura, humedad, pH y volteos; el sistema genera **alertas**
   cuando la temperatura supera 70 °C o la humedad sale del rango 40 %–65 %, y muestra la curva de temperatura
   de cada pila. Al terminar, se registran los **lotes de abono** producidos.
5. **Dashboard y reportes:** indicadores calculados por el backend desde Oracle: **toneladas de residuo
   desviadas de vertederos**, **kilos de abono producido**, rendimiento residuo → abono, recolecciones del mes,
   pilas por fase y alertas. Reportes: **consolidado de toneladas transformadas por mes**, consolidado por
   proveedor, exportación a CSV e impresión, y trazabilidad de cada lote.

## 3. Arquitectura

Arquitectura de tres capas, tal como exige el proyecto integrador:

**Usuario → Frontend → API REST (FastAPI) → Oracle Database → API REST → Frontend**

- **Frontend:** HTML5, CSS3, JavaScript y Bootstrap 5. Diseño responsive (computador y celular, con menú tipo
  hamburguesa). Consume la API con `fetch()` enviando el token JWT. Gráficos con Chart.js. Nunca se conecta
  directamente a la base de datos.
- **Backend:** Python con FastAPI, organizado en capas: `routers` (endpoints y permisos), `schemas` (validación
  con Pydantic), `services` (reglas de negocio y consultas SQL), `models` (catálogos del dominio), `database`
  (pool de conexiones) y `core` (configuración, seguridad y manejo de errores). 42 endpoints documentados
  automáticamente con Swagger/OpenAPI.
- **Base de datos:** Oracle Database 23ai Free ejecutándose en Docker, conectada con el controlador oficial
  `oracledb`. 7 tablas: ROLES, USUARIOS, PROVEEDORES, RECOLECCIONES, PILAS_COMPOST, MONITOREO_PILAS y
  LOTES_ABONO, con llaves primarias y foráneas, restricciones UNIQUE y CHECK, e índices.

### Decisión técnica importante
El primer avance del equipo intentaba consultar Oracle APEX a través de servicios web ORDS ejecutando el
programa `curl` desde Python para evadir el firewall de apex.oracle.com. Esto generaba errores intermitentes
(el servidor devolvía páginas HTML de bloqueo en lugar de datos) y no cumplía el requisito de usar el
controlador oficial `oracledb`. Se rediseñó la conexión: ahora el backend se conecta directamente a Oracle con
`oracledb` (modo thin, sin instalar Oracle Client), usando un pool de conexiones y credenciales en variables de
entorno. La base corre en Docker para que todo el equipo tenga exactamente el mismo entorno con un solo comando.

## 4. Seguridad y validación
- Contraseñas cifradas con bcrypt; la API nunca devuelve el hash.
- Token JWT con expiración; en cada petición se verifica que el usuario siga activo.
- Permisos por rol validados en el backend: 401 sin sesión, 403 sin permiso. El frontend además oculta los
  botones y páginas no permitidos.
- Validación en tres niveles: navegador (HTML5), backend (Pydantic + reglas de negocio) y Oracle (restricciones).
- Consultas con variables de enlace para evitar inyección SQL.
- Credenciales en el archivo `.env`, excluido de GitHub. CORS limitado al origen del frontend.
- Errores traducidos a mensajes claros en español, sin mostrar detalles técnicos al usuario.

**Reglas de negocio:** un residuo rechazado no entra a ninguna pila; la clasificación condicionado o rechazado
exige observaciones; no se reciben residuos de proveedores inactivos; no se asigna residuo ni se registran
mediciones en pilas finalizadas; solo se producen lotes de pilas en maduración o finalizadas; el abono de una
pila no puede superar el residuo que recibió; el recolector solo edita sus propias recolecciones; no se eliminan
proveedores o usuarios con historial (se desactivan).

## 5. Datos de demostración (escenario mayo–octubre de 2026)
- 8 proveedores en Cali, Palmira, Candelaria, Jamundí, Pradera, Yumbo, El Cerrito y Florida (7 activos).
- 48 recolecciones: **40,37 toneladas desviadas de vertederos** (estiércol 17,2 t; bagazo 8,6 t; frutas 5,5 t;
  hortalizas 4,9 t; mixto 4,1 t) y 0,26 t rechazadas.
- 6 pilas, una en cada fase (2 finalizadas), con 74 mediciones; la pila P-2026-05 (termofílica) tiene una
  alerta activa: 71,8 °C y humedad de 38,5 %.
- 4 lotes de abono con **6.400 kg producidos** (3.300 kg disponibles) y un **rendimiento de 34,8 %**, un valor
  típico del compostaje, porque el material pierde agua y masa durante el proceso.
- Reporte mensual: mayo 7,14 t; junio 8,39 t; julio 8,57 t; agosto 6,65 t (3.100 kg de abono); septiembre
  5,60 t (3.300 kg de abono); octubre 4,04 t.

## 6. Pruebas
- **24 pruebas automatizadas** con pytest sobre la base Oracle real: login correcto, incorrecto y de usuario
  inactivo; CRUD completo; validación de datos incorrectos; reglas de negocio; duplicados (409); control de
  acceso por rol (403); filtros; dashboard; reportes y trazabilidad. Todas aprobadas.
- **Colección de Postman** con 34 peticiones y 41 verificaciones automáticas. Todas aprobadas.
- Pruebas funcionales en el navegador, incluida la vista en celular, y prueba de resiliencia: si Oracle se
  detiene la API responde 503 con un mensaje claro y se recupera sola al volver la base de datos.

## 7. Trabajo colaborativo
Repositorio en GitHub con la estructura exigida (frontend, backend, database, docs, tests), README con
instrucciones de instalación, `.gitignore`, `.env.example` y registro de integrantes y responsabilidades:
- Integrante 1: base de datos Oracle, seguridad, autenticación y módulo de usuarios y roles.
- Integrante 2: módulos de proveedores y recolecciones (API, validaciones y pantallas).
- Integrante 3: pilas, monitoreo, lotes, dashboard, reportes y pruebas.

## 8. Impacto y trabajo futuro
BioCompost permite demostrar con datos el impacto ambiental de la planta (toneladas que no llegaron al
vertedero), mejorar el proceso (alertas de temperatura y humedad) y dar confianza al comprador del abono
(trazabilidad del lote hasta sus proveedores). Mejoras futuras: despliegue en la nube con HTTPS, aplicación
móvil para registrar el pesaje sin conexión, lectura automática de sensores de temperatura, códigos QR en los
bultos de abono para consultar su trazabilidad y estimación de CO₂ evitado.

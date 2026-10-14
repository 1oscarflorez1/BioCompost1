# BioCompost

**Sistema de Trazabilidad de Recolección de Residuos Orgánicos y Compostaje Agrícola**

Proyecto Integrador · Desarrollo Web y Sistemas Móviles · Universidad Cooperativa de Colombia, sede Cali · 2026-2

BioCompost gestiona la ruta de recolección de desechos orgánicos en zonas rurales y agrícolas (plazas de mercado,
fincas y empresas agroindustriales) y controla su transformación en abono orgánico: desde que el residuo se pesa
en la báscula hasta que sale convertido en un lote de compost, con trazabilidad completa del origen.

```
Usuario → Frontend (HTML5 + Bootstrap + JS) → API REST (FastAPI) → Oracle Database → API REST → Frontend
```

---

## Integrantes y responsabilidades

| Integrante | Rol en el equipo | Responsabilidades principales |
|---|---|---|
| _(Robin Guzman)_ | Base de datos y seguridad | Modelo E-R, scripts Oracle (`database/`), conexión `oracledb`, autenticación JWT, módulo de usuarios y roles, login |
| _(Oscar Florez)_ | Operación (proveedores y recolecciones) | Módulos 2 y 3: API, validaciones, reglas de negocio y pantallas de proveedores y recolecciones |
| _(Sergio Rosas)_ | Compostaje y análisis | Módulos 4 y 5: pilas, monitoreo, lotes, trazabilidad, dashboard, reportes y pruebas (pytest / Postman) |

---

## Módulos funcionales

| # | Módulo | Qué hace | Tablas |
|---|---|---|---|
| 1 | Autenticación y perfiles | Inicio de sesión con JWT, roles **Administrador de planta** y **Recolector**, gestión de usuarios | `ROLES`, `USUARIOS` |
| 2 | Proveedores de residuos | CRUD de puntos de recolección (plaza de mercado, finca, agroindustria) y su tipo de residuo | `PROVEEDORES` |
| 3 | Recolecciones y entradas | CRUD del pesaje: fecha, origen, tipo, clasificación (apto / condicionado / rechazado) y pila destino | `RECOLECCIONES` |
| 4 | Control de pilas de compostaje | CRUD de pilas por fase de maduración, monitoreo de temperatura, humedad, pH y volteos, lotes de abono | `PILAS_COMPOST`, `MONITOREO_PILAS`, `LOTES_ABONO` |
| 5 | Dashboard y reportes | Toneladas desviadas de vertederos, kilos de abono producido, rendimiento, alertas y reportes consolidados | (consultas sobre todas) |

**Filtros y reportes destacados:** filtrar pilas por fase de maduración, reporte consolidado de toneladas
transformadas por mes, reporte por proveedor, búsqueda y filtros en todos los módulos, exportación a CSV y
trazabilidad de cada lote hasta sus proveedores de origen.

### Roles y permisos

| Acción | Administrador de planta | Recolector |
|---|:-:|:-:|
| Dashboard y reportes | ✅ | ✅ |
| Consultar proveedores, pilas, monitoreo y lotes | ✅ | ✅ |
| Registrar recolecciones | ✅ | ✅ |
| Editar recolecciones | ✅ todas | ✅ solo las propias |
| Eliminar recolecciones | ✅ | ❌ |
| Crear / editar / eliminar proveedores, pilas, mediciones y lotes | ✅ | ❌ |
| Gestionar usuarios y roles | ✅ | ❌ |

Los permisos se validan en el **backend** (respuesta `403`); el frontend además oculta las opciones no permitidas.

---

## Tecnologías

| Capa | Tecnología |
|---|---|
| Frontend | HTML5, CSS3, JavaScript (`fetch`), Bootstrap 5.3, Bootstrap Icons, Chart.js |
| Backend | Python 3.10+, FastAPI, Pydantic v2, Uvicorn |
| Base de datos | Oracle Database 23ai Free (Docker) — compatible con Oracle XE 21c y 19c |
| Conexión | `oracledb` (controlador oficial de Oracle, modo *thin*: no requiere Instant Client) |
| Seguridad | JWT (`PyJWT`), contraseñas cifradas con `bcrypt`, variables de entorno (`.env`) |
| Documentación API | Swagger / OpenAPI (automática de FastAPI) |
| Pruebas | `pytest` (21 pruebas de integración) y colección de Postman (29 peticiones) |

---

## Estructura del repositorio

```
BioCompost1/
├── frontend/
│   ├── index.html            # Dashboard
│   ├── login.html
│   ├── pages/                # proveedores, recolecciones, pilas, monitoreo, lotes, reportes, usuarios
│   ├── css/styles.css
│   ├── js/                   # config, api (fetch), auth (sesión), ui (utilidades) + un archivo por página
│   └── assets/logo.svg
├── backend/
│   ├── main.py               # Aplicación FastAPI, CORS y registro de routers
│   ├── init_db.py            # Ejecuta los scripts SQL en Oracle
│   ├── core/                 # config (.env), security (bcrypt/JWT), errores (manejo global)
│   ├── database/             # connection.py: pool de conexiones oracledb
│   ├── models/               # catalogos.py: valores permitidos del dominio (enums)
│   ├── schemas/              # Pydantic: validación de entrada y formato de salida
│   ├── services/             # Lógica de negocio y consultas SQL
│   ├── routers/              # Endpoints REST por módulo + dependencias de seguridad
│   └── requirements.txt
├── database/
│   ├── 01_tables.sql         # Tablas (modelo físico)
│   ├── 02_constraints.sql    # PK/FK, UNIQUE, CHECK, índices y comentarios
│   ├── 03_data.sql           # Datos iniciales de prueba
│   └── 04_queries.sql        # Consultas relevantes (filtros, dashboard, reportes, trazabilidad)
├── docs/                     # Modelo de datos, arquitectura, API, pruebas y material de presentación
├── tests/                    # pytest + colección de Postman
├── docker-compose.yml        # Oracle Database Free para desarrollo
├── .env.example              # Plantilla de variables de entorno
└── README.md
```

---

## Instalación y ejecución

### Inicio rápido en Windows (doble clic)

| Archivo | Cuándo usarlo |
|---|---|
| `instalar.bat` | Solo la primera vez en cada computador: crea `.env`, el entorno de Python, instala librerías, enciende Oracle en Docker y carga los datos. |
| `iniciar.bat` | Cada vez que vaya a usar el sistema: enciende Oracle, la API y el frontend, y abre el navegador. |
| `detener.bat` | Para apagar todo (los datos se conservan). |
| `reiniciar_datos.bat` | Para volver a los datos de prueba originales (por ejemplo, antes de la presentación). |

Requisito: tener **Docker Desktop abierto** ("Engine running"). Abajo están los mismos pasos explicados uno por uno.

### Requisitos

- [Python 3.10 o superior](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (para la base de datos Oracle), **o** un Oracle XE / Oracle Database ya instalado
- Un navegador moderno

### 1. Variables de entorno

```bash
cp .env.example .env
```

Edite `.env` y cambie las contraseñas (`DB_PASSWORD`, `ORACLE_ADMIN_PASSWORD`) y la clave `JWT_SECRET`.
Para generar una clave segura: `python -c "import secrets; print(secrets.token_hex(32))"`.

### 2. Base de datos Oracle

Con Docker (la primera vez descarga la imagen y tarda unos minutos):

```bash
docker compose up -d
```

Espere a que el contenedor quede *healthy* (`docker ps`). El contenedor crea automáticamente el usuario de la
aplicación definido en `DB_USER` / `DB_PASSWORD`.

> **Sin Docker:** cree un usuario en su Oracle (por ejemplo en `XEPDB1`) y ajuste `DB_DSN` en `.env`
> (`localhost:1521/XEPDB1`). También puede ejecutar los scripts de `database/` en orden desde SQL Developer.

### 3. Backend (FastAPI)

> En Windows, si `python --version` muestra una versión menor a 3.10, cree el entorno con el lanzador `py`
> indicando una versión instalada, por ejemplo `py -3.12 -m venv .venv` (ver versiones con `py -0`).

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
python init_db.py               # crea las tablas y carga los datos de prueba
uvicorn main:app --reload
```

- API: <http://127.0.0.1:8000>
- **Swagger:** <http://127.0.0.1:8000/docs> — use `POST /api/auth/login`, copie el `access_token` y péguelo en **Authorize**.
- Estado de la conexión con Oracle: <http://127.0.0.1:8000/api/salud>

### 4. Frontend

En otra terminal, desde la raíz del repositorio:	

```bash
python -m http.server 5500 --directory frontend
```

Abra <http://localhost:5500/login.html>. (También funciona con la extensión *Live Server* de VS Code en el puerto 5500.)
Si la API corre en otra dirección, cambie `API_URL` en `frontend/js/config.js` y agregue el origen a `CORS_ORIGINS` en `.env`.

### Usuarios de prueba

| Correo | Contraseña | Rol |
|---|---|---|
| admin@biocompost.com | `Admin2026*` | Administrador de planta |
| carlos.rodriguez@biocompost.com | `Recolector2026*` | Recolector |
| diana.torres@biocompost.com | `Recolector2026*` | Recolector |
| pedro.salazar@biocompost.com | `Recolector2026*` | Recolector **inactivo** (para probar el bloqueo) |

---

## Pruebas

Con la base de datos y los datos iniciales cargados:

```bash
backend\.venv\Scripts\python -m pytest -v
```

21 pruebas de integración: inicio de sesión, CRUD, validación de datos incorrectos, reglas de negocio,
control de acceso por rol, filtros, dashboard, reportes y trazabilidad.

**Postman:** importe `tests/BioCompost.postman_collection.json`, inicie la API y use *Run collection*
(29 peticiones con 35 verificaciones automáticas). Detalle en [docs/pruebas.md](docs/pruebas.md).

---

## Documentación

- [Modelo de datos (E-R, lógico y físico)](docs/modelo_datos.md)
- [Arquitectura y decisiones de diseño](docs/arquitectura.md)
- [API REST: endpoints, códigos HTTP y permisos](docs/api.md)
- [Plan y evidencias de pruebas](docs/pruebas.md)
- [Material para la sustentación](docs/presentacion/)

---

## Seguridad aplicada

- Contraseñas almacenadas con **bcrypt** (nunca en texto plano) y nunca devueltas por la API.
- Autenticación con **token JWT** (expira en 8 horas por defecto); el usuario se verifica en cada petición, de modo
  que si el administrador lo desactiva pierde el acceso de inmediato.
- Autorización por **rol** en cada endpoint (`401` sin sesión, `403` sin permiso).
- Validación en el **frontend** (HTML5 + Bootstrap), en el **backend** (Pydantic + reglas de negocio) y en
  **Oracle** (PK, FK, UNIQUE, CHECK).
- Consultas con **variables de enlace** (`:parametro`) para prevenir inyección SQL.
- Credenciales fuera del código (`.env` excluido de Git). CORS restringido a los orígenes del frontend.
- Mensajes de error claros en español, sin exponer trazas ni códigos internos de Oracle.

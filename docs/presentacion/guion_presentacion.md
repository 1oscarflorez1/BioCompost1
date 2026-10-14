# Guion de sustentación — BioCompost

**Duración total:** ~20 minutos + preguntas · **Expositores:** 3 · Las diapositivas corresponden a las que genera
el prompt de NotebookLM (`prompt_notebooklm.md`).

> Reemplacen `[Integrante 1]`, `[Integrante 2]` e `[Integrante 3]` por sus nombres. El texto entre comillas es
> una guía para hablar con naturalidad: no lo lean palabra por palabra. Las cifras sí deben decirse exactas.

| Bloque | Expositor | Diapositivas | Tiempo |
|---|---|---|---|
| Problema, arquitectura, base de datos y seguridad | [Integrante 1] | 1 – 7 | 5,5 min |
| Backend, validación, proveedores y recolecciones | [Integrante 2] | 8 – 11 | 4 min |
| Pilas, trazabilidad, dashboard, frontend y pruebas | [Integrante 3] | 12 – 16 | 4 min |
| Demostración en vivo (por turnos) | Los tres | 17 | 6 min |
| Conclusiones y preguntas | Los tres | 18 – 19 | 1 min + preguntas |

---

## Antes de entrar al salón (lista de verificación)

Hacerlo 30 minutos antes en el computador que se va a proyectar:

- [ ] Docker Desktop abierto ("Engine running").
- [ ] Doble clic en **`iniciar.bat`** (enciende Oracle, la API y el frontend). Equivale a los comandos manuales:
      `docker compose up -d`, `uvicorn main:app` y `python -m http.server 5500 --directory frontend`.
- [ ] Doble clic en **`reiniciar_datos.bat`** para que las cifras coincidan con las diapositivas.
- [ ] Doble clic en **`consola_oracle.bat`** y dejar esa ventana abierta para el paso 6 del turno 2.
- [ ] <http://127.0.0.1:8000/api/salud> debe decir `"base_datos":"ok"`.
- [ ] Pestañas abiertas en este orden: (1) <http://localhost:5500/login.html>, (2) <http://127.0.0.1:8000/docs>,
      (3) GitHub del repositorio, (4) terminal con `pytest -v` ya ejecutado, (5) Postman con el resultado de *Run collection*.
- [ ] Zoom del navegador al 110–125 % para que se lea desde el fondo del salón.
- [ ] Sesión cerrada en el navegador (botón *Cerrar sesión*) para empezar la demo desde el login.
- [ ] Hay internet (Bootstrap y Chart.js se cargan desde CDN). Si no hay, usar el **plan B** del final.

---

## [Integrante 1] — Diapositivas 1 a 7 (5,5 min)

**Diapositiva 1 · Portada**
"Buenos días. Somos [Integrante 1], [Integrante 2] e [Integrante 3] y les presentamos **BioCompost**, un sistema
web de trazabilidad para la recolección de residuos orgánicos y su transformación en abono."

**Diapositiva 2 · El problema**
"En el Valle del Cauca las plazas de mercado, las fincas y los trapiches producen todos los días residuos
orgánicos: cáscaras de fruta, hortalizas, estiércol y bagazo de caña. Casi todo termina en el relleno sanitario.
Esos residuos podrían convertirse en compost, pero una planta de compostaje necesita saber cuánto recibe, de
dónde viene, cómo avanza cada pila y cuánto abono produce. Si eso se lleva en papel se pierde la trazabilidad y
no se puede demostrar el impacto ambiental."

**Diapositiva 3 · Objetivo y alcance**
"Nuestro objetivo fue construir una aplicación Full Stack que siga el residuo desde que se pesa en la báscula
hasta que sale convertido en un lote de abono. La organizamos en cinco módulos: autenticación y perfiles,
proveedores, recolecciones, control de pilas de compostaje, y dashboard con reportes."

**Diapositiva 4 · Arquitectura**
"Usamos la arquitectura de tres capas que pide el proyecto. El usuario trabaja en un frontend hecho con HTML,
Bootstrap y JavaScript; ese frontend solo habla con nuestra API REST hecha en FastAPI, y la API es la única que
se conecta a Oracle. El frontend nunca toca la base de datos directamente."

**Diapositiva 5 · Decisión técnica**
"Queremos contarles una decisión importante. En el primer avance intentamos usar Oracle APEX en la nube a través
de servicios ORDS, y para que el firewall no nos bloqueara ejecutábamos `curl` desde Python. Funcionaba a ratos:
muchas veces el servidor devolvía una página HTML de bloqueo en vez de datos y no pudimos avanzar. Además no
cumplía el requisito de usar el controlador oficial `oracledb`. Entonces cambiamos el enfoque: Oracle Database
corre en un contenedor Docker, y el backend se conecta con `oracledb` usando un pool de conexiones y las
credenciales en un archivo `.env`. Ahora cualquier integrante levanta la misma base con un solo comando."

**Diapositiva 6 · Modelo de datos**
"Diseñamos la base antes de programar. Tiene siete tablas: roles, usuarios, proveedores, recolecciones,
pilas de compostaje, monitoreo de pilas y lotes de abono. La columna vertebral es la cadena de trazabilidad:
un **proveedor** origina **recolecciones**, las recolecciones alimentan una **pila**, y la pila produce **lotes
de abono**. Por eso, de cualquier bulto de abono podemos saber de qué fincas o plazas vino."

**Diapositiva 7 · Integridad y seguridad**
"La integridad la garantiza Oracle: llaves primarias y foráneas, restricciones UNIQUE para que no se repita un
NIT o un correo, y restricciones CHECK, por ejemplo que el peso sea mayor que cero o que la humedad esté entre 0
y 100. Las contraseñas se guardan cifradas con bcrypt. Al iniciar sesión la API entrega un token JWT, y cada
petición se valida según el rol: el **Administrador de planta** gestiona todo, y el **Recolector** registra sus
recolecciones y consulta. Si alguien no ha iniciado sesión recibe 401, y si no tiene permiso, 403.
Un detalle de diseño: cada rol tiene un **código interno fijo**, que es el que usan los permisos, y un **nombre
visible** que el administrador puede editar junto con la descripción. Así puede llamar al rol 'Jefe de planta' sin
que nadie pierda ni gane accesos. Le doy la palabra a [Integrante 2]."

---

## [Integrante 2] — Diapositivas 8 a 11 (4 min)

**Diapositiva 8 · Backend con FastAPI**
"El backend está organizado por capas. Los **routers** definen los endpoints y quién puede usarlos; los
**schemas** de Pydantic validan los datos que llegan; los **services** tienen las reglas de negocio y las
consultas SQL; y la carpeta **database** maneja la conexión con Oracle. En total son 42 endpoints, todos
documentados automáticamente en Swagger. Usamos los códigos HTTP correctos: 201 al crear, 404 si no existe,
409 si hay un duplicado, 422 si un dato es inválido."

**Diapositiva 9 · Validación en tres niveles**
"Validamos tres veces. Primero el navegador: campos obligatorios, rangos y formatos. Segundo el backend: aunque
alguien se salte el formulario, por ejemplo desde Postman, Pydantic rechaza un peso negativo o una fecha futura.
Y tercero Oracle, con sus restricciones. Los errores se traducen a mensajes claros en español y el formulario
marca en rojo el campo exacto, sin mostrar errores técnicos de la base de datos."

**Diapositiva 10 · Proveedores**
"El módulo de proveedores registra los puntos de recolección: plazas de mercado, fincas y agroindustrias, con
su dirección, municipio, contacto y tipo de residuo principal. Tiene búsqueda por nombre, NIT o contacto, y
filtros por tipo, residuo, municipio y estado. Un detalle: si un proveedor ya tiene recolecciones no se puede
borrar, porque se perdería la trazabilidad; el sistema sugiere desactivarlo."

**Diapositiva 11 · Recolecciones**
"Aquí se registra cada pesaje: proveedor, fecha, kilos, tipo de residuo y clasificación: apto, condicionado o
rechazado. Programamos reglas de negocio reales: un residuo rechazado no puede entrar a una pila, si es
condicionado o rechazado hay que escribir el motivo, no se reciben residuos de proveedores inactivos y no se
puede agregar material a una pila que ya terminó. Además, un recolector solo puede editar las recolecciones que
él mismo registró. Sigue [Integrante 3]."

---

## [Integrante 3] — Diapositivas 12 a 16 (4 min)

**Diapositiva 12 · Pilas y monitoreo**
"Cada pila pasa por las fases del compostaje: **mesofílica**, cuando arranca; **termofílica**, cuando supera los
45 grados y se eliminan los patógenos; luego **enfriamiento**, **maduración** y **finalizada**. El sistema
permite filtrar las pilas por fase, y registrar mediciones de temperatura, humedad, pH y volteos. Si la
temperatura pasa de 70 grados o la humedad sale del rango de 40 a 65 por ciento, se genera una alerta."

**Diapositiva 13 · Lotes y trazabilidad**
"Cuando la pila madura se registran los lotes de abono. Desde un lote se ve su trazabilidad completa: de qué
pila salió, qué recolecciones la alimentaron y qué proveedores aportaron. El sistema también valida que el abono
no supere el residuo que recibió la pila. En nuestros datos el rendimiento es de **34,8 %**, que es lo normal,
porque en el compostaje el material pierde agua y masa."

**Diapositiva 14 · Dashboard y reportes**
"El dashboard muestra indicadores calculados por el backend directamente desde Oracle: **40,37 toneladas
desviadas de vertederos** y **6.400 kilos de abono producido**, entre otros. El reporte que pedía el proyecto,
el consolidado de toneladas transformadas por mes, se puede filtrar por año, exportar a CSV e imprimir. También
hay un reporte por proveedor."

**Diapositiva 15 · Frontend responsive**
"El frontend usa Bootstrap, así que se adapta al computador y al celular, donde el menú se vuelve tipo
hamburguesa; esto es útil para el recolector que trabaja en campo. Todo se carga con `fetch` enviando el token,
y las opciones que el rol no permite ni siquiera aparecen."

**Diapositiva 16 · Pruebas**
"Probamos el sistema con 24 pruebas automatizadas en pytest contra la base Oracle real: login correcto, login
incorrecto, usuario inactivo, CRUD completo, datos inválidos, duplicados, control de acceso por rol, filtros,
reportes y trazabilidad. Todas pasan. También tenemos una colección de Postman con 34 peticiones y 41
verificaciones. Incluso probamos apagar la base de datos: la API responde con un mensaje claro y se recupera sola.
Ahora se los mostramos funcionando."

---

## Diapositiva 17 · Demostración en vivo (6 min, por turnos)

**Historia de la demo:** "Hoy llegó un camión de la Plaza de Mercado El Porvenir con 520 kilos de frutas.
Sigámoslo dentro del sistema."

### Turno 1 — [Integrante 1]: inicio de sesión y roles (1,5 min)
1. En `login.html` pulsar **Ingresar** con los campos vacíos → "Fíjense que valida antes de llamar a la API".
2. Iniciar sesión como `pedro.salazar@biocompost.com` → mensaje de **usuario inactivo** (403).
3. Iniciar sesión como **recolector** `carlos.rodriguez@biocompost.com` → "El menú no tiene *Usuarios*".
4. Escribir en la barra de direcciones `.../pages/usuarios.html` → **Acceso restringido**.
   "Y aunque intentara llamar la API directamente, el backend responde 403."

### Turno 2 — [Integrante 2]: registrar la recolección (2 min)
1. (Sigue la sesión de Carlos) **Recolecciones → Registrar recolección**.
2. Proveedor *Plaza de Mercado El Porvenir* → "El tipo de residuo se llena solo: Frutas".
3. Peso `-5` → **Guardar** → el campo se marca en rojo. Corregir a `520`.
4. Cambiar clasificación a **Rechazado** → "La pila se bloquea y las observaciones se vuelven obligatorias".
   Volver a **Apto** y elegir la pila **P-2026-06**. Guardar → mensaje de éxito y el registro aparece primero.
5. Mostrar que en las filas de otros recolectores **no aparece** el botón de editar ni el de eliminar.
6. **Comprobar que llegó a Oracle:** en la ventana de `consola_oracle.bat` (abierta antes de empezar) escribir
   `SELECT id_recoleccion, fecha_recoleccion, peso_kg, tipo_residuo FROM recolecciones ORDER BY id_recoleccion DESC FETCH FIRST 1 ROWS ONLY;`
   → "Ahí está el registro de 520 kg que acabamos de hacer desde la página: viajó del formulario a FastAPI y quedó
   guardado en Oracle."
7. Pestaña de **Swagger**: "Aquí están los 42 endpoints. Por ejemplo `POST /api/recolecciones` con un tipo de
   residuo inventado devuelve 422 con el error de cada campo." (Tenerlo ejecutado de antemano.)

### Turno 3 — [Integrante 3]: compostaje, trazabilidad y reportes (2,5 min)
1. Cerrar sesión e ingresar como **administrador** `admin@biocompost.com`.
2. **Dashboard**: "Las recolecciones del mes subieron con el registro que acabamos de hacer". Señalar la
   **alerta** de la pila P-2026-05.
3. **Pilas de compostaje** → botón **Termofílica** → "Este es el filtro por fase que pedía el proyecto".
4. Ícono de gráfico de P-2026-05 → **Monitoreo**: mostrar la curva de temperatura con la línea de 70 °C.
5. **Lotes de abono** → ícono de trazabilidad de **L-2026-001** → "4 proveedores, 10 recolecciones, 8.880 kg,
   pila P-2026-01, rendimiento 34,9 %".
6. **Reportes** → consolidado mensual 2026 → **Exportar CSV**.
7. (Si sobra tiempo) mostrar la terminal con `24 passed` y el resumen de Postman.

### Demostración opcional — [Integrante 1]: gestión de roles (30 s)
Úsenla si sobra tiempo o si el docente pregunta por la "gestión de roles". Requiere la sesión del administrador.
1. **Usuarios y roles** → en la tarjeta *Administrador de planta* pulsar **Editar**.
2. Cambiar el nombre a **Jefe de planta** → **Guardar**. "El nombre cambia en la tarjeta, en la tabla y en el
   menú, pero el código interno sigue siendo ADMINISTRADOR, así que no perdemos ningún permiso."
3. Volver a dejar *Administrador de planta* (o ejecutar `reiniciar_datos.bat` después de la presentación).

---

## Diapositivas 18 y 19 · Conclusiones y preguntas (1 min)

- **[Integrante 1]:** "Aprendimos que diseñar bien la base de datos primero nos ahorró problemas después, y que
  cuando una tecnología no funciona hay que tomar la decisión de cambiarla a tiempo."
- **[Integrante 2]:** "Entendimos la importancia de validar en el backend: el frontend ayuda al usuario, pero la
  seguridad real está en la API y en la base de datos."
- **[Integrante 3]:** "Y vimos el valor de los datos: con BioCompost una planta puede demostrar cuántas toneladas
  dejó de enviar al vertedero. Como trabajo futuro proponemos desplegarlo en la nube con HTTPS, una app móvil para
  el pesaje sin conexión, sensores de temperatura y códigos QR en los bultos de abono. Muchas gracias, quedamos
  atentos a sus preguntas."

---

## Banco de preguntas probables

| Pregunta | Responde | Respuesta corta |
|---|---|---|
| ¿Por qué el frontend no se conecta directo a Oracle? | 1 | Por seguridad y arquitectura: las credenciales quedarían expuestas en el navegador. La API valida, autoriza y es la única que conoce la base. |
| ¿Cómo guardan las contraseñas? | 1 | Con bcrypt, que aplica una sal aleatoria y es lento a propósito. Nunca se guarda ni se devuelve la contraseña. |
| ¿Qué es un JWT y qué pasa cuando vence? | 1 | Un token firmado con nuestra clave secreta que incluye el id y el rol, con fecha de expiración. Si vence, la API responde 401 y el frontend lleva al login. |
| Si desactivan a un usuario con sesión abierta, ¿sigue entrando? | 1 | No: en cada petición el backend consulta que el usuario siga activo. |
| ¿Cómo gestionan los roles? ¿Se pueden crear o borrar? | 1 | El administrador asigna roles a los usuarios y edita el nombre y la descripción de cada rol. No se crean ni se borran, porque cada rol necesita permisos programados en el backend; un rol nuevo no tendría permisos definidos. |
| ¿Qué pasa si el administrador renombra su propio rol? | 1 | Nada malo: los permisos dependen del código interno (`ADMINISTRADOR`), que no se edita; solo cambia el nombre visible. Lo comprueba una prueba automática. |
| ¿Cómo evitan la inyección SQL? | 2 | Todas las consultas usan variables de enlace (`:parametro`) de oracledb; el texto del usuario nunca se concatena al SQL. |
| ¿Por qué 422 y no 400 en la validación? | 2 | 422 es el estándar de FastAPI para datos con formato o rango inválido; usamos 400 para reglas de negocio, como asignar residuo a una pila finalizada. |
| ¿Qué pasa si borran una pila? | 1 | Sus mediciones se borran en cascada y sus recolecciones quedan sin pila (`SET NULL`). Si ya produjo lotes, Oracle no lo permite y la API responde 409. |
| ¿Dónde están las credenciales de la base? | 1 | En el archivo `.env`, que está en `.gitignore`; en GitHub solo está `.env.example` sin claves reales. |
| ¿Por qué no usaron un ORM? | 2 | Para escribir y explicar el SQL de Oracle directamente (CTE, `FULL OUTER JOIN`, funciones analíticas); las mismas consultas están en `04_queries.sql`. |
| ¿Cómo se calcula "toneladas desviadas"? | 3 | Suma del peso de las recolecciones aptas y condicionadas, porque son las que entran a compostaje; las rechazadas no cuentan. |
| ¿Por qué el rendimiento es solo 34,8 %? | 3 | Es normal: durante el compostaje se evapora agua y la materia orgánica se descompone en CO₂; por eso el compost pesa mucho menos que el residuo inicial. |
| ¿Por qué la alerta a 70 °C? | 3 | Por encima de ese valor los microorganismos benéficos se inhiben y el proceso se frena; los límites están en `models/catalogos.py` y se pueden ajustar. |
| ¿Cómo prueban que funciona? | 3 | 24 pruebas pytest contra la base real y la colección de Postman; además la demo muestra el flujo completo Frontend → API → Oracle → Frontend. |
| ¿Funciona sin Docker? | 1 | Sí: con Oracle XE instalado basta crear el usuario, cambiar `DB_DSN` en `.env` y ejecutar `init_db.py` o los scripts en SQL Developer. |
| ¿Qué le falta para producción? | 3 | HTTPS, despliegue en un servidor, copias de seguridad, renovación de tokens y registro de auditoría. |

---

## Plan B (si algo falla en la demo)

- **No hay internet:** las páginas se ven sin estilos porque Bootstrap viene de CDN. Mostrar Swagger (funciona
  local) y las capturas de pantalla guardadas en `docs/evidencias/`.
- **La API dice "No hay conexión con el servidor":** revisar que `uvicorn` siga corriendo y que la URL sea la de
  `frontend/js/config.js`.
- **503 "No fue posible conectar con la base de datos":** `docker start biocompost-oracle`, esperar a `healthy`.
- **Los números no coinciden con las diapositivas:** se agregaron datos en ensayos; ejecutar `python init_db.py`.
- **Nervios o tiempo corto:** priorizar login → registrar recolección → dashboard → trazabilidad del lote.

---

## Antes de la entrega: contribuciones en GitHub

El enunciado exige que cada integrante tenga commits identificables. Recomendación: cada uno sube su parte
desde **su propia cuenta**, con commits descriptivos y, si es posible, en una rama con *pull request*:

| Integrante | Rama sugerida | Archivos |
|---|---|---|
| [Integrante 1] | `feature/base-datos-seguridad` | `database/`, `docker-compose.yml`, `.env.example`, los archivos `.bat`, `backend/core/`, `backend/database/`, `backend/init_db.py`, `backend/main.py`, `backend/routers/auth.py`, `backend/routers/dependencias.py`, `backend/routers/usuarios.py`, `backend/services/auth_service.py`, `backend/services/usuarios_service.py`, `backend/schemas/auth.py`, `backend/schemas/usuario.py`, `backend/schemas/base.py`, `frontend/login.html`, `frontend/js/login.js`, `frontend/js/auth.js`, `frontend/pages/usuarios.html`, `frontend/js/usuarios.js`, `docs/modelo_datos.md` |
| [Integrante 2] | `feature/proveedores-recolecciones` | `backend/models/`, `backend/routers/proveedores.py`, `backend/routers/recolecciones.py`, `backend/services/proveedores_service.py`, `backend/services/recolecciones_service.py`, `backend/schemas/proveedor.py`, `backend/schemas/recoleccion.py`, `frontend/css/`, `frontend/assets/`, `frontend/js/config.js`, `frontend/js/api.js`, `frontend/js/ui.js`, `frontend/pages/proveedores.html`, `frontend/pages/recolecciones.html` y sus `.js`, `docs/api.md`, `docs/arquitectura.md` |
| [Integrante 3] | `feature/pilas-reportes-pruebas` | `backend/routers/pilas.py`, `monitoreos.py`, `lotes.py`, `reportes.py`, sus `services` y `schemas`, `frontend/index.html`, `frontend/js/dashboard.js`, `frontend/pages/pilas.html`, `monitoreo.html`, `lotes.html`, `reportes.html` y sus `.js`, `tests/`, `pytest.ini`, `docs/pruebas.md`, `docs/presentacion/`, `README.md` |

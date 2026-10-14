# Plan y evidencias de pruebas

Se aplicaron tres tipos de prueba sobre el sistema completo (Frontend → FastAPI → Oracle):

1. **Pruebas automatizadas de la API** con `pytest` (`tests/test_api.py`): 24 casos.
2. **Colección de Postman** (`tests/BioCompost.postman_collection.json`): 34 peticiones con 41 verificaciones.
3. **Pruebas funcionales en el navegador** (manuales, guiadas por la tabla de la sección 3).

Todas las pruebas usan la base de datos Oracle real con los datos de `database/03_data.sql`, y dejan la base
como estaba (los registros que crean los eliminan al final).

## 1. Cómo ejecutarlas

```bash
# Requisitos: Oracle en ejecución (docker compose up -d) y datos cargados (python backend/init_db.py)
backend\.venv\Scripts\python -m pytest -v
```

Postman: *Import* → `tests/BioCompost.postman_collection.json` → con la API encendida, *Run collection*.
Desde consola también puede usarse Newman: `npx newman run tests/BioCompost.postman_collection.json`.

## 2. Resultado de la última ejecución

| Herramienta | Casos | Resultado |
|---|---|---|
| pytest | 24 pruebas | **24 aprobadas** (≈ 4 s) |
| Postman / Newman | 34 peticiones, 41 aserciones | **41 aprobadas, 0 fallidas** |
| Base de datos detenida | `GET /api/salud` y endpoints | **503** con mensaje claro; la API se recupera sola al reiniciar Oracle |

## 3. Casos de prueba (sección 11 del enunciado)

| # | Requisito | Caso | Resultado esperado | pytest | Postman |
|---|---|---|---|:-:|:-:|
| 1 | Inicio de sesión | Credenciales correctas | 200 + token JWT + rol, sin exponer el hash | ✅ | ✅ |
| 2 | Inicio de sesión | Contraseña incorrecta | 401 "Correo o contraseña incorrectos" | ✅ | ✅ |
| 3 | Inicio de sesión | Usuario inactivo | 403 | ✅ | ✅ |
| 4 | Seguridad | Petición sin token / con token falso | 401 | ✅ | ✅ |
| 5 | Creación | Registrar proveedor | 201 con el id generado por Oracle | ✅ | ✅ |
| 6 | Consulta | Consultar por id y buscar con filtros | 200 y solo los registros que cumplen el filtro | ✅ | ✅ |
| 7 | Actualización | Modificar municipio y estado del proveedor | 200 con los datos nuevos | ✅ | ✅ |
| 8 | Eliminación | Eliminar proveedor y consultarlo después | 200 y luego 404 | ✅ | ✅ |
| 9 | Creación | Recolector registra una recolección | 201; el recolector se toma del token | ✅ | ✅ |
| 10 | Validación | Peso negativo, fecha futura, tipo de residuo inexistente | 422 con el error de cada campo | ✅ | ✅ |
| 11 | Validación | Residuo RECHAZADO asignado a una pila | 422 | ✅ | — |
| 12 | Validación | Pila FINALIZADA sin fecha de finalización | 422 | — | ✅ |
| 13 | Regla de negocio | Asignar residuo a una pila FINALIZADA | 400 | ✅ | — |
| 14 | Regla de negocio | Lote de abono de una pila en fase TERMOFÍLICA | 400 | ✅ | — |
| 15 | Integridad (Oracle) | NIT de proveedor duplicado | 409 "Ya existe un proveedor con ese documento" | ✅ | ✅ |
| 16 | Integridad (Oracle) | Eliminar proveedor con recolecciones | 409 sugiriendo desactivarlo | ✅ | — |
| 17 | Control de acceso | Recolector consulta usuarios | 403 | ✅ | ✅ |
| 18 | Control de acceso | Recolector crea una pila | 403 | ✅ | ✅ |
| 19 | Control de acceso | Recolector edita una recolección de otro usuario | 403 | ✅ | — |
| 20 | Control de acceso | Recolector elimina una recolección | 403 (el administrador sí puede: 200) | ✅ | ✅ |
| 21 | Filtros | Pilas por fase de maduración | Solo pilas de la fase pedida | ✅ | ✅ |
| 22 | Dashboard | Indicadores desde el backend | Toneladas desviadas, kg de abono, 6 meses | ✅ | ✅ |
| 23 | Reportes | Consolidado mensual | La suma de los meses coincide con el total | ✅ | ✅ |
| 24 | Trazabilidad | Lote → pila → recolecciones → proveedores | Lista de recolecciones de origen | ✅ | ✅ |
| 25 | Gestión de roles | Administrador edita nombre y descripción de un rol | 200; el código interno no cambia y los usuarios muestran el nombre nuevo | ✅ | ✅ |
| 26 | Gestión de roles | Renombrar el rol del administrador | Conserva todos sus permisos (200 en `/api/usuarios`) | ✅ | — |
| 27 | Gestión de roles | Nombre muy corto / repetido / rol inexistente | 422 / 409 / 404 | ✅ | ✅ (422) |
| 28 | Control de acceso | Recolector intenta editar un rol | 403 | ✅ | ✅ |

## 4. Pruebas funcionales en el navegador

| Pantalla | Acción | Resultado verificado |
|---|---|---|
| Login | Enviar el formulario vacío | Campos marcados en rojo con mensaje, no se llama a la API |
| Login | Credenciales correctas | Redirige al dashboard con el nombre y rol del usuario |
| Dashboard | Cargar | Indicadores, gráfico mensual, residuo por tipo, pilas por fase y alerta de la pila P-2026-05 |
| Proveedores | Crear → duplicar NIT → editar → eliminar | Mensaje de éxito; el duplicado muestra el error 409 dentro del formulario |
| Recolecciones | Elegir clasificación RECHAZADO | Se deshabilita la pila y las observaciones pasan a ser obligatorias |
| Pilas | Botones de fase | Filtra la tabla con `GET /api/pilas?fase=...` y muestra el conteo por fase |
| Monitoreo | Seleccionar una pila | Curvas de temperatura y humedad con los límites recomendados |
| Lotes | Ver trazabilidad | Proveedores → recolecciones → pila → lote, con rendimiento |
| Reportes | Cambiar año, exportar CSV, imprimir | Tabla con totales, gráfico y archivo CSV |
| Usuarios y roles | Editar el rol "Administrador de planta" a "Jefe de planta" | Mensaje de éxito; el nombre cambia en la tarjeta, la tabla y el menú, y el administrador conserva sus accesos |
| Usuarios (como recolector) | Abrir la página | "Acceso restringido"; el menú no muestra la opción |
| Recolecciones (como recolector) | Revisar acciones | Solo puede editar sus propios registros y no ve botones de eliminar |
| Celular (375 px) | Navegar | Menú lateral tipo hamburguesa, tarjetas apiladas y tablas con desplazamiento |

## 5. Evidencias sugeridas para la entrega

Tomar capturas de pantalla de: Swagger con el login y un `POST` exitoso, la ejecución de `pytest -v`, el resumen
de *Run collection* de Postman, el dashboard, un formulario con errores de validación, el mensaje 403 del
recolector y la vista en celular. Guardarlas en `docs/evidencias/`.

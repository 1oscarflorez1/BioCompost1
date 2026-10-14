# API REST — BioCompost

Documentación interactiva (Swagger / OpenAPI) generada por FastAPI: <http://127.0.0.1:8000/docs>
· Esquema OpenAPI: <http://127.0.0.1:8000/openapi.json>

Todas las rutas (excepto login y salud) requieren el encabezado `Authorization: Bearer <token>`.

## Autenticación

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| POST | `/api/auth/login` | Inicia sesión; devuelve `access_token` y datos del usuario | Público |
| GET | `/api/auth/me` | Usuario de la sesión actual | Todos |

## Usuarios y roles

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| GET | `/api/roles` | Roles con su código, nombre y número de usuarios | Admin |
| GET | `/api/roles/{id}` | Consultar un rol | Admin |
| PUT | `/api/roles/{id}` | Editar nombre visible y descripción (el código interno no cambia) | Admin |
| GET | `/api/usuarios?texto=&id_rol=&activo=` | Listar y buscar | Admin |
| GET | `/api/usuarios/{id}` | Consultar | Admin |
| POST | `/api/usuarios` | Crear (contraseña con letras y números, mín. 8) | Admin |
| PUT | `/api/usuarios/{id}` | Actualizar (contraseña opcional) | Admin |
| DELETE | `/api/usuarios/{id}` | Eliminar | Admin |

## Proveedores

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| GET | `/api/proveedores?texto=&tipo_proveedor=&tipo_residuo=&municipio=&activo=` | Listar, buscar y filtrar | Todos |
| GET | `/api/proveedores/{id}` | Consultar | Todos |
| POST | `/api/proveedores` | Registrar | Admin |
| PUT | `/api/proveedores/{id}` | Actualizar | Admin |
| DELETE | `/api/proveedores/{id}` | Eliminar (409 si tiene recolecciones) | Admin |

## Recolecciones

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| GET | `/api/recolecciones?texto=&fecha_desde=&fecha_hasta=&id_proveedor=&id_pila=&tipo_residuo=&clasificacion=&sin_pila=` | Listar y filtrar | Todos |
| GET | `/api/recolecciones/{id}` | Consultar | Todos |
| POST | `/api/recolecciones` | Registrar (el recolector se toma del token) | Todos |
| PUT | `/api/recolecciones/{id}` | Actualizar (el recolector solo las suyas) | Todos* |
| DELETE | `/api/recolecciones/{id}` | Eliminar | Admin |

## Pilas de compostaje y monitoreo

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| GET | `/api/pilas?fase=&texto=&solo_activas=` | Listar y **filtrar por fase de maduración** | Todos |
| GET | `/api/pilas/{id}` | Consultar (kilos recibidos, última medición, alerta) | Todos |
| POST | `/api/pilas` | Crear | Admin |
| PUT | `/api/pilas/{id}` | Actualizar / cambiar fase / finalizar | Admin |
| DELETE | `/api/pilas/{id}` | Eliminar (409 si produjo lotes) | Admin |
| GET | `/api/monitoreos?id_pila=&fecha_desde=&fecha_hasta=&solo_alertas=` | Listar mediciones | Todos |
| GET | `/api/monitoreos/{id}` | Consultar | Todos |
| POST | `/api/monitoreos` | Registrar temperatura, humedad, pH y volteo | Admin |
| PUT | `/api/monitoreos/{id}` | Actualizar | Admin |
| DELETE | `/api/monitoreos/{id}` | Eliminar | Admin |

## Lotes de abono

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| GET | `/api/lotes?texto=&estado=&calidad=&id_pila=` | Listar y filtrar | Todos |
| GET | `/api/lotes/{id}` | Consultar | Todos |
| GET | `/api/lotes/{id}/trazabilidad` | Pila, recolecciones y proveedores de origen | Todos |
| POST | `/api/lotes` | Registrar | Admin |
| PUT | `/api/lotes/{id}` | Actualizar | Admin |
| DELETE | `/api/lotes/{id}` | Eliminar | Admin |

## Dashboard y reportes

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| GET | `/api/dashboard` | Indicadores, gráficos, alertas y últimas recolecciones | Todos |
| GET | `/api/reportes/mensual?anio=2026` | **Consolidado de toneladas transformadas por mes** | Todos |
| GET | `/api/reportes/proveedores?fecha_desde=&fecha_hasta=` | Residuo aportado por proveedor | Todos |
| GET | `/api/reportes/anios` | Años con información | Todos |
| GET | `/api/salud` | Estado de la API y de la conexión con Oracle | Público |

## Códigos HTTP utilizados

| Código | Significado en BioCompost | Ejemplo |
|---|---|---|
| 200 | Consulta, actualización o eliminación correcta | `GET /api/pilas` |
| 201 | Registro creado | `POST /api/proveedores` |
| 400 | Regla de negocio no cumplida | Asignar residuo a una pila finalizada |
| 401 | Sin sesión, token inválido o expirado, credenciales incorrectas | Login con contraseña errada |
| 403 | El rol no tiene permiso / usuario inactivo | Recolector en `/api/usuarios` |
| 404 | El registro no existe | `GET /api/pilas/999` |
| 409 | Conflicto con datos existentes | NIT duplicado, eliminar proveedor con historial |
| 422 | Datos con formato o rango inválido (validación) | Peso negativo, fecha futura |
| 500 | Error interno (sin detalles técnicos para el usuario) | — |
| 503 | La base de datos no está disponible | Oracle apagado |

## Formato de errores

Todos los errores devuelven un JSON con `detail` (mensaje para el usuario). Los de validación incluyen además
la lista de campos, que el frontend usa para marcar en rojo cada campo:

```json
{
  "detail": "Datos no válidos. peso_kg: Debe ser mayor que 0; tipo_residuo: Valor no permitido. Opciones: 'FRUTAS', 'HORTALIZAS', 'ESTIERCOL', 'BAGAZO' o 'MIXTO'",
  "errores": [
    {"campo": "peso_kg", "mensaje": "Debe ser mayor que 0"},
    {"campo": "tipo_residuo", "mensaje": "Valor no permitido. Opciones: 'FRUTAS', 'HORTALIZAS', 'ESTIERCOL', 'BAGAZO' o 'MIXTO'"}
  ]
}
```

## Ejemplo de uso

```http
POST /api/auth/login
Content-Type: application/json

{"correo": "admin@biocompost.com", "contrasena": "Admin2026*"}
```

```http
POST /api/recolecciones
Authorization: Bearer eyJhbGciOi...
Content-Type: application/json

{
  "id_proveedor": 1,
  "id_pila": 6,
  "fecha_recoleccion": "2026-10-12",
  "peso_kg": 420.5,
  "tipo_residuo": "FRUTAS",
  "clasificacion": "APTO"
}
```

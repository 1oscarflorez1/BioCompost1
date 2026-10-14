"""Pruebas funcionales de la API BioCompost (sección 11 del enunciado)."""
from datetime import date, timedelta

from conftest import ADMIN, INACTIVO

HOY = date.today().isoformat()


def _id_pila(cliente, cabeceras, fase):
    pilas = cliente.get("/api/pilas", params={"fase": fase}, headers=cabeceras).json()
    assert pilas, f"Los datos de prueba deben tener una pila en fase {fase}"
    return pilas[0]["id_pila"]


# ---------------------------------------------------------------------------
# 1. Inicio de sesión
# ---------------------------------------------------------------------------
def test_api_y_base_de_datos_en_linea(cliente):
    assert cliente.get("/api/salud").json() == {"api": "ok", "base_datos": "ok"}


def test_login_correcto_devuelve_token_y_rol(cliente):
    respuesta = cliente.post("/api/auth/login", json=ADMIN)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["token_type"] == "bearer" and datos["access_token"]
    assert datos["usuario"]["rol"] == "ADMINISTRADOR"
    assert datos["usuario"]["rol_nombre"]
    assert "contrasena_hash" not in datos["usuario"]


def test_login_con_contrasena_incorrecta(cliente):
    respuesta = cliente.post("/api/auth/login", json={**ADMIN, "contrasena": "incorrecta1"})
    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "Correo o contraseña incorrectos"


def test_login_de_usuario_inactivo(cliente):
    assert cliente.post("/api/auth/login", json=INACTIVO).status_code == 403


def test_endpoint_protegido_sin_token(cliente):
    assert cliente.get("/api/proveedores").status_code == 401


def test_token_invalido(cliente):
    respuesta = cliente.get("/api/proveedores", headers={"Authorization": "Bearer token-falso"})
    assert respuesta.status_code == 401


# ---------------------------------------------------------------------------
# 2. CRUD completo (crear, consultar, actualizar, eliminar)
# ---------------------------------------------------------------------------
def test_crud_completo_de_proveedor(cliente, admin):
    nuevo = {
        "nombre": "Finca Prueba Automatizada",
        "tipo_proveedor": "FINCA",
        "documento": "909090909-9",
        "direccion": "Vereda La Prueba km 1",
        "municipio": "Palmira",
        "tipo_residuo": "HORTALIZAS",
    }
    # Crear -> 201
    creado = cliente.post("/api/proveedores", json=nuevo, headers=admin)
    assert creado.status_code == 201, creado.text
    id_proveedor = creado.json()["id_proveedor"]
    try:
        # Consultar -> 200
        consultado = cliente.get(f"/api/proveedores/{id_proveedor}", headers=admin)
        assert consultado.status_code == 200
        assert consultado.json()["nombre"] == nuevo["nombre"]

        # Buscar con filtros
        encontrados = cliente.get("/api/proveedores", params={"texto": "prueba automatizada"}, headers=admin).json()
        assert [p["id_proveedor"] for p in encontrados] == [id_proveedor]

        # Actualizar -> 200
        actualizado = cliente.put(
            f"/api/proveedores/{id_proveedor}", json={**nuevo, "municipio": "Cali", "activo": "N"}, headers=admin
        )
        assert actualizado.status_code == 200
        assert actualizado.json()["municipio"] == "Cali" and actualizado.json()["activo"] == "N"
    finally:
        # Eliminar -> 200 y luego ya no existe -> 404
        assert cliente.delete(f"/api/proveedores/{id_proveedor}", headers=admin).status_code == 200
    assert cliente.get(f"/api/proveedores/{id_proveedor}", headers=admin).status_code == 404


def test_recolector_registra_y_edita_su_recoleccion(cliente, recolector, admin):
    id_pila = _id_pila(cliente, admin, "MESOFILICA")
    datos = {"id_proveedor": 1, "id_pila": id_pila, "fecha_recoleccion": HOY, "peso_kg": 350.5, "tipo_residuo": "FRUTAS"}
    creada = cliente.post("/api/recolecciones", json=datos, headers=recolector)
    assert creada.status_code == 201, creada.text
    recoleccion = creada.json()
    assert recoleccion["recolector"] == "Carlos Rodríguez"  # se toma del token, no del formulario
    try:
        editada = cliente.put(f"/api/recolecciones/{recoleccion['id_recoleccion']}",
                              json={**datos, "peso_kg": 400}, headers=recolector)
        assert editada.status_code == 200 and editada.json()["peso_kg"] == 400
    finally:
        # Solo el administrador puede eliminar
        assert cliente.delete(f"/api/recolecciones/{recoleccion['id_recoleccion']}", headers=recolector).status_code == 403
        assert cliente.delete(f"/api/recolecciones/{recoleccion['id_recoleccion']}", headers=admin).status_code == 200


# ---------------------------------------------------------------------------
# 3. Validación de datos incorrectos
# ---------------------------------------------------------------------------
def test_validacion_de_recoleccion_con_datos_incorrectos(cliente, recolector):
    manana = (date.today() + timedelta(days=1)).isoformat()
    respuesta = cliente.post(
        "/api/recolecciones",
        json={"id_proveedor": 1, "fecha_recoleccion": manana, "peso_kg": -5, "tipo_residuo": "PLASTICO"},
        headers=recolector,
    )
    assert respuesta.status_code == 422
    campos = {e["campo"] for e in respuesta.json()["errores"]}
    assert {"fecha_recoleccion", "peso_kg", "tipo_residuo"} <= campos


def test_residuo_rechazado_no_puede_ir_a_una_pila(cliente, recolector):
    respuesta = cliente.post(
        "/api/recolecciones",
        json={"id_proveedor": 1, "id_pila": 1, "fecha_recoleccion": HOY, "peso_kg": 10,
              "tipo_residuo": "FRUTAS", "clasificacion": "RECHAZADO", "observaciones": "Contaminado"},
        headers=recolector,
    )
    assert respuesta.status_code == 422
    assert "RECHAZADO" in respuesta.json()["detail"]


def test_no_se_asigna_residuo_a_pila_finalizada(cliente, recolector, admin):
    id_pila = _id_pila(cliente, admin, "FINALIZADA")
    respuesta = cliente.post(
        "/api/recolecciones",
        json={"id_proveedor": 1, "id_pila": id_pila, "fecha_recoleccion": HOY, "peso_kg": 10, "tipo_residuo": "FRUTAS"},
        headers=recolector,
    )
    assert respuesta.status_code == 400


def test_lote_solo_de_pilas_maduras(cliente, admin):
    id_pila = _id_pila(cliente, admin, "TERMOFILICA")
    respuesta = cliente.post(
        "/api/lotes",
        json={"id_pila": id_pila, "codigo_lote": "L-TEST-01", "fecha_produccion": HOY, "kilos_producidos": 10},
        headers=admin,
    )
    assert respuesta.status_code == 400


def test_documento_duplicado_devuelve_409(cliente, admin):
    existente = cliente.get("/api/proveedores", headers=admin).json()[0]
    respuesta = cliente.post(
        "/api/proveedores",
        json={"nombre": "Duplicado", "tipo_proveedor": "FINCA", "documento": existente["documento"],
              "direccion": "Calle 1 # 2-3", "municipio": "Cali", "tipo_residuo": "FRUTAS"},
        headers=admin,
    )
    assert respuesta.status_code == 409


def test_no_se_elimina_proveedor_con_recolecciones(cliente, admin):
    con_entregas = next(p for p in cliente.get("/api/proveedores", headers=admin).json() if p["num_recolecciones"] > 0)
    respuesta = cliente.delete(f"/api/proveedores/{con_entregas['id_proveedor']}", headers=admin)
    assert respuesta.status_code == 409
    assert "desactivarlo" in respuesta.json()["detail"]


# ---------------------------------------------------------------------------
# 4. Control de acceso según el rol
# ---------------------------------------------------------------------------
def test_recolector_no_gestiona_usuarios(cliente, recolector):
    assert cliente.get("/api/usuarios", headers=recolector).status_code == 403


def test_recolector_no_crea_pilas(cliente, recolector):
    respuesta = cliente.post("/api/pilas", json={"codigo": "P-X", "fecha_inicio": HOY}, headers=recolector)
    assert respuesta.status_code == 403


def test_recolector_no_edita_recolecciones_ajenas(cliente, recolector):
    ajena = next(r for r in cliente.get("/api/recolecciones", headers=recolector).json()
                 if r["recolector"] == "Diana Torres")
    datos = {k: ajena[k] for k in ("id_proveedor", "id_pila", "fecha_recoleccion", "peso_kg",
                                    "tipo_residuo", "clasificacion", "observaciones")}
    respuesta = cliente.put(f"/api/recolecciones/{ajena['id_recoleccion']}", json=datos, headers=recolector)
    assert respuesta.status_code == 403


# ---------------------------------------------------------------------------
# 5. Gestión de roles (nombre visible y descripción editables)
# ---------------------------------------------------------------------------
def _rol(cliente, admin, codigo):
    return next(r for r in cliente.get("/api/roles", headers=admin).json() if r["codigo"] == codigo)


def test_admin_edita_nombre_y_descripcion_de_rol(cliente, admin):
    original = _rol(cliente, admin, "RECOLECTOR")
    try:
        respuesta = cliente.put(f"/api/roles/{original['id_rol']}",
                                json={"nombre": "Operario de recolección", "descripcion": "Recoge y pesa residuos"},
                                headers=admin)
        assert respuesta.status_code == 200
        assert respuesta.json()["nombre"] == "Operario de recolección"
        assert respuesta.json()["codigo"] == "RECOLECTOR"  # el código interno no cambia
        usuarios = cliente.get("/api/usuarios", params={"id_rol": original["id_rol"]}, headers=admin).json()
        assert all(u["rol_nombre"] == "Operario de recolección" for u in usuarios)
    finally:
        cliente.put(f"/api/roles/{original['id_rol']}",
                    json={"nombre": original["nombre"], "descripcion": original["descripcion"]}, headers=admin)


def test_renombrar_rol_administrador_no_quita_permisos(cliente, admin):
    original = _rol(cliente, admin, "ADMINISTRADOR")
    try:
        cliente.put(f"/api/roles/{original['id_rol']}", json={"nombre": "Jefe de planta"}, headers=admin)
        # Sigue teniendo acceso a lo exclusivo del administrador
        assert cliente.get("/api/usuarios", headers=admin).status_code == 200
        sesion = cliente.post("/api/auth/login", json=ADMIN).json()["usuario"]
        assert sesion["rol"] == "ADMINISTRADOR" and sesion["rol_nombre"] == "Jefe de planta"
    finally:
        cliente.put(f"/api/roles/{original['id_rol']}",
                    json={"nombre": original["nombre"], "descripcion": original["descripcion"]}, headers=admin)


def test_validaciones_al_editar_rol(cliente, admin, recolector):
    administrador = _rol(cliente, admin, "ADMINISTRADOR")
    rol_recolector = _rol(cliente, admin, "RECOLECTOR")
    ruta = f"/api/roles/{rol_recolector['id_rol']}"
    assert cliente.put(ruta, json={"nombre": "ab"}, headers=admin).status_code == 422
    assert cliente.put(ruta, json={"nombre": administrador["nombre"]}, headers=admin).status_code == 409
    assert cliente.put(ruta, json={"nombre": "Otro nombre"}, headers=recolector).status_code == 403
    assert cliente.put("/api/roles/999", json={"nombre": "No existe"}, headers=admin).status_code == 404


# ---------------------------------------------------------------------------
# 6. Filtros, dashboard y reportes
# ---------------------------------------------------------------------------
def test_filtro_de_pilas_por_fase(cliente, recolector):
    pilas = cliente.get("/api/pilas", params={"fase": "FINALIZADA"}, headers=recolector).json()
    assert pilas and all(p["fase"] == "FINALIZADA" for p in pilas)


def test_dashboard_entrega_indicadores(cliente, recolector):
    datos = cliente.get("/api/dashboard", headers=recolector).json()
    assert datos["indicadores"]["toneladas_desviadas"] > 0
    assert datos["indicadores"]["kg_abono_producido"] > 0
    assert len(datos["por_mes"]) == 6


def test_reporte_mensual_cuadra_con_sus_totales(cliente, admin):
    reporte = cliente.get("/api/reportes/mensual", params={"anio": 2026}, headers=admin).json()
    suma = round(sum(m["kg_desviados"] for m in reporte["meses"]) / 1000, 2)
    assert reporte["totales"]["toneladas_desviadas"] == suma
    assert reporte["totales"]["kg_abono_producido"] == sum(m["kg_abono_producido"] for m in reporte["meses"])
    # El total del reporte coincide con el indicador del dashboard
    dashboard = cliente.get("/api/dashboard", headers=admin).json()
    assert reporte["totales"]["toneladas_desviadas"] == dashboard["indicadores"]["toneladas_desviadas"]


def test_trazabilidad_de_lote(cliente, recolector):
    lote = cliente.get("/api/lotes", headers=recolector).json()[0]
    traza = cliente.get(f"/api/lotes/{lote['id_lote']}/trazabilidad", headers=recolector).json()
    assert traza["recolecciones"] and traza["num_proveedores"] >= 1

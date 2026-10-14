"""Errores de la aplicación y manejadores globales.

Objetivo: devolver siempre un código HTTP apropiado y un mensaje claro en
español, sin exponer al usuario detalles técnicos (trazas, errores ORA-xxxxx).
"""
import logging

import oracledb
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

log = logging.getLogger("biocompost")


# ---------------------------------------------------------------------------
# Excepciones que lanzan los servicios
# ---------------------------------------------------------------------------
class ErrorAplicacion(Exception):
    codigo_http = 400

    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje = mensaje


class ReglaNegocio(ErrorAplicacion):
    codigo_http = 400


class NoAutorizado(ErrorAplicacion):
    codigo_http = 401


class Prohibido(ErrorAplicacion):
    codigo_http = 403


class NoEncontrado(ErrorAplicacion):
    codigo_http = 404


class Conflicto(ErrorAplicacion):
    codigo_http = 409


# ---------------------------------------------------------------------------
# Traducción de errores de Oracle (restricciones de integridad)
# ---------------------------------------------------------------------------
DUPLICADOS = {
    "UQ_USUARIOS_CORREO": "Ya existe un usuario registrado con ese correo",
    "UQ_PROVEEDORES_DOC": "Ya existe un proveedor con ese documento (NIT/CC)",
    "UQ_PILAS_CODIGO": "Ya existe una pila con ese código",
    "UQ_LOTES_CODIGO": "Ya existe un lote de abono con ese código",
    "UQ_ROLES_NOMBRE": "Ya existe un rol con ese nombre",
}

REGISTROS_ASOCIADOS = {
    "FK_RECOLECCIONES_PROVEEDOR": "El proveedor tiene recolecciones registradas. Puede desactivarlo en lugar de eliminarlo",
    "FK_RECOLECCIONES_USUARIO": "El usuario tiene recolecciones registradas. Puede desactivarlo en lugar de eliminarlo",
    "FK_MONITOREO_USUARIO": "El usuario tiene monitoreos registrados. Puede desactivarlo en lugar de eliminarlo",
    "FK_LOTES_PILA": "La pila tiene lotes de abono asociados y no puede eliminarse",
    "FK_USUARIOS_ROL": "El rol tiene usuarios asignados y no puede eliminarse",
}


def _buscar_mensaje(texto: str, mensajes: dict, por_defecto: str) -> str:
    for restriccion, mensaje in mensajes.items():
        if restriccion in texto:
            return mensaje
    return por_defecto


def traducir_error_oracle(error: oracledb.Error) -> tuple[int, str]:
    detalle = error.args[0] if error.args else None
    codigo = getattr(detalle, "code", 0)
    texto = str(getattr(detalle, "message", error)).upper()

    if codigo == 1:  # ORA-00001: violación de UNIQUE
        return 409, _buscar_mensaje(texto, DUPLICADOS, "El registro ya existe (dato duplicado)")
    if codigo == 2292:  # ORA-02292: existen registros hijos
        return 409, _buscar_mensaje(texto, REGISTROS_ASOCIADOS, "No se puede eliminar porque tiene información asociada")
    if codigo == 2291:  # ORA-02291: la llave foránea no existe
        return 400, "El registro relacionado (proveedor, pila, usuario o rol) no existe"
    if codigo == 2290:  # ORA-02290: violación de CHECK
        return 400, "Uno de los valores no cumple las reglas de la base de datos"
    if codigo == 1400:  # ORA-01400: NULL en columna obligatoria
        return 400, "Falta un dato obligatorio"
    if isinstance(error, (oracledb.OperationalError, oracledb.InterfaceError)):
        return 503, "No fue posible conectar con la base de datos. Intente nuevamente en unos minutos"
    return 500, "Error interno del servidor"


# ---------------------------------------------------------------------------
# Traducción de errores de validación de Pydantic
# ---------------------------------------------------------------------------
TRADUCCIONES = {
    "missing": "Campo obligatorio",
    "string_too_short": "Debe tener al menos {min_length} caracteres",
    "string_too_long": "Debe tener máximo {max_length} caracteres",
    "greater_than": "Debe ser mayor que {gt}",
    "greater_than_equal": "Debe ser mayor o igual a {ge}",
    "less_than": "Debe ser menor que {lt}",
    "less_than_equal": "Debe ser menor o igual a {le}",
    "enum": "Valor no permitido. Opciones: {expected}",
    "literal_error": "Valor no permitido. Opciones: {expected}",
    "string_pattern_mismatch": "Formato no válido",
    "date_parsing": "Fecha no válida (use el formato AAAA-MM-DD)",
    "date_from_datetime_parsing": "Fecha no válida (use el formato AAAA-MM-DD)",
    "int_parsing": "Debe ser un número entero",
    "float_parsing": "Debe ser un número",
    "json_invalid": "El cuerpo de la petición no es un JSON válido",
}


def _texto(valor) -> str:
    if isinstance(valor, float) and valor.is_integer():
        valor = int(valor)  # 0.0 -> 0
    return str(valor).replace(" or ", " o ")


def _traducir_validacion(error: dict) -> str:
    tipo = error.get("type", "")
    if error.get("input") is None and tipo.endswith("_type"):
        return "Campo obligatorio"
    if tipo == "value_error":
        mensaje = error.get("msg", "")
        if "email" in mensaje.lower():
            return "Correo electrónico no válido"
        return mensaje.removeprefix("Value error, ")
    if tipo in TRADUCCIONES:
        contexto = {k: _texto(v) for k, v in error.get("ctx", {}).items()}
        try:
            return TRADUCCIONES[tipo].format(**contexto)
        except KeyError:
            pass
    return error.get("msg", "Dato no válido")


# ---------------------------------------------------------------------------
# Registro de manejadores en la aplicación
# ---------------------------------------------------------------------------
def registrar_manejadores(app: FastAPI):
    @app.exception_handler(ErrorAplicacion)
    async def manejar_error_aplicacion(request: Request, exc: ErrorAplicacion):
        cabeceras = {"WWW-Authenticate": "Bearer"} if exc.codigo_http == 401 else None
        return JSONResponse(status_code=exc.codigo_http, content={"detail": exc.mensaje}, headers=cabeceras)

    @app.exception_handler(RequestValidationError)
    async def manejar_validacion(request: Request, exc: RequestValidationError):
        errores = []
        for error in exc.errors():
            campo = ".".join(str(p) for p in error.get("loc", []) if p not in ("body", "query", "path"))
            errores.append({"campo": campo or "general", "mensaje": _traducir_validacion(error)})
        resumen = "; ".join(
            e["mensaje"] if e["campo"] == "general" else f"{e['campo']}: {e['mensaje']}" for e in errores
        )
        return JSONResponse(status_code=422, content={"detail": f"Datos no válidos. {resumen}", "errores": errores})

    @app.exception_handler(oracledb.Error)
    async def manejar_error_oracle(request: Request, exc: oracledb.Error):
        codigo, mensaje = traducir_error_oracle(exc)
        if codigo >= 500:
            log.error("Error de base de datos en %s %s: %s", request.method, request.url.path, exc)
        return JSONResponse(status_code=codigo, content={"detail": mensaje})

    @app.exception_handler(Exception)
    async def manejar_error_inesperado(request: Request, exc: Exception):
        log.exception("Error no controlado en %s %s", request.method, request.url.path)
        return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})

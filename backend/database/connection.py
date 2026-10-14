"""Conexión a Oracle Database con el controlador oficial `oracledb` (modo thin).

Se usa un pool de conexiones para no abrir una conexión nueva en cada petición.
Todas las consultas usan variables de enlace (:nombre), lo que evita la
inyección SQL.
"""
from contextlib import contextmanager

import oracledb

from core import config

_pool = None


def iniciar_pool():
    """Crea el pool de conexiones (se llama al arrancar la API)."""
    global _pool
    if _pool is None:
        _pool = oracledb.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            dsn=config.DB_DSN,
            min=1,
            max=5,
            increment=1,
        )
    return _pool


def cerrar_pool():
    global _pool
    if _pool is not None:
        _pool.close(force=True)
        _pool = None


@contextmanager
def obtener_conexion():
    """Entrega una conexión del pool. Hace COMMIT si todo sale bien y ROLLBACK si hay error."""
    conexion = iniciar_pool().acquire()
    try:
        yield conexion
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()  # la devuelve al pool


def _filas_como_diccionarios(cursor):
    """Hace que cada fila se devuelva como dict {columna_en_minuscula: valor}."""
    columnas = [col[0].lower() for col in cursor.description]
    cursor.rowfactory = lambda *fila: dict(zip(columnas, fila))


def consultar(sql: str, parametros: dict | None = None) -> list[dict]:
    """Ejecuta un SELECT y devuelve todas las filas."""
    with obtener_conexion() as conexion, conexion.cursor() as cursor:
        cursor.execute(sql, parametros or {})
        _filas_como_diccionarios(cursor)
        return cursor.fetchall()


def consultar_uno(sql: str, parametros: dict | None = None) -> dict | None:
    """Ejecuta un SELECT y devuelve la primera fila (o None)."""
    filas = consultar(sql, parametros)
    return filas[0] if filas else None


def ejecutar(sql: str, parametros: dict | None = None) -> int:
    """Ejecuta un INSERT/UPDATE/DELETE y devuelve el número de filas afectadas."""
    with obtener_conexion() as conexion, conexion.cursor() as cursor:
        cursor.execute(sql, parametros or {})
        return cursor.rowcount


def clausula_where(condiciones: list[str]) -> str:
    """Une las condiciones de los filtros: ['a = :a', 'b = :b'] -> ' WHERE a = :a AND b = :b'."""
    return " WHERE " + " AND ".join(condiciones) if condiciones else ""


def insertar(sql: str, parametros: dict, columna_id: str) -> int:
    """Ejecuta un INSERT y devuelve el id generado por la columna IDENTITY."""
    with obtener_conexion() as conexion, conexion.cursor() as cursor:
        nuevo_id = cursor.var(oracledb.NUMBER)
        cursor.execute(f"{sql} RETURNING {columna_id} INTO :nuevo_id", {**parametros, "nuevo_id": nuevo_id})
        return int(nuevo_id.getvalue()[0])

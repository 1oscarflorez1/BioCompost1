"""Crea las tablas y carga los datos iniciales en Oracle.

Ejecuta, en orden, los scripts de la carpeta /database:
    01_tables.sql -> 02_constraints.sql -> 03_data.sql

Uso (desde la carpeta backend, con el entorno virtual activo):
    python init_db.py

ATENCIÓN: 01_tables.sql borra y vuelve a crear las tablas (se pierden los datos).
"""
from pathlib import Path

import oracledb

from core import config

CARPETA_SQL = Path(__file__).resolve().parent.parent / "database"
SCRIPTS = ["01_tables.sql", "02_constraints.sql", "03_data.sql"]
TABLAS = ["ROLES", "USUARIOS", "PROVEEDORES", "PILAS_COMPOST", "RECOLECCIONES", "MONITOREO_PILAS", "LOTES_ABONO"]


def leer_sentencias(ruta: Path) -> list[str]:
    """Separa un script estilo SQL*Plus en sentencias.

    - Las sentencias SQL terminan con ';' al final de la línea.
    - Los bloques PL/SQL (BEGIN/DECLARE) terminan con una línea que solo tiene '/'.
    """
    sentencias, actual, en_bloque = [], [], False
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        limpia = linea.strip()
        if not actual and (not limpia or limpia.startswith("--")):
            continue
        if not actual and limpia.upper().split(" ")[0] in ("BEGIN", "DECLARE"):
            en_bloque = True
        if en_bloque:
            if limpia == "/":
                sentencias.append("\n".join(actual))
                actual, en_bloque = [], False
            else:
                actual.append(linea)
            continue
        actual.append(linea)
        if limpia.endswith(";"):
            sentencias.append("\n".join(actual).rstrip().rstrip(";"))
            actual = []
    return sentencias


def main():
    print(f"Conectando a Oracle ({config.DB_DSN}) con el usuario {config.DB_USER}...")
    with oracledb.connect(user=config.DB_USER, password=config.DB_PASSWORD, dsn=config.DB_DSN) as conexion:
        cursor = conexion.cursor()
        for nombre in SCRIPTS:
            sentencias = leer_sentencias(CARPETA_SQL / nombre)
            print(f"  -> {nombre}: {len(sentencias)} sentencias")
            for sentencia in sentencias:
                if sentencia.strip().upper() == "COMMIT":
                    conexion.commit()
                    continue
                try:
                    cursor.execute(sentencia)
                except oracledb.DatabaseError as error:
                    print(f"\nError ejecutando en {nombre}:\n{sentencia[:300]}\n{error}")
                    raise SystemExit(1)
            conexion.commit()

        print("\nRegistros por tabla:")
        for tabla in TABLAS:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            print(f"  {tabla:<16} {cursor.fetchone()[0]}")
    print("\nBase de datos lista.")


if __name__ == "__main__":
    main()

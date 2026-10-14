"""Modelos del dominio: valores permitidos en el sistema.

Coinciden con las restricciones CHECK de Oracle (database/02_constraints.sql),
de modo que la validación se hace en el backend y también en la base de datos.
"""
from enum import Enum


class Rol(str, Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    RECOLECTOR = "RECOLECTOR"


class TipoProveedor(str, Enum):
    PLAZA_MERCADO = "PLAZA_MERCADO"
    FINCA = "FINCA"
    AGROINDUSTRIA = "AGROINDUSTRIA"


class TipoResiduo(str, Enum):
    FRUTAS = "FRUTAS"
    HORTALIZAS = "HORTALIZAS"
    ESTIERCOL = "ESTIERCOL"
    BAGAZO = "BAGAZO"
    MIXTO = "MIXTO"


class Clasificacion(str, Enum):
    APTO = "APTO"
    CONDICIONADO = "CONDICIONADO"
    RECHAZADO = "RECHAZADO"


class FasePila(str, Enum):
    MESOFILICA = "MESOFILICA"
    TERMOFILICA = "TERMOFILICA"
    ENFRIAMIENTO = "ENFRIAMIENTO"
    MADURACION = "MADURACION"
    FINALIZADA = "FINALIZADA"


class CalidadLote(str, Enum):
    PREMIUM = "PREMIUM"
    ESTANDAR = "ESTANDAR"
    REPROCESO = "REPROCESO"


class EstadoLote(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    DESPACHADO = "DESPACHADO"


# Rangos recomendados para el proceso de compostaje (generan alertas)
TEMPERATURA_MAXIMA = 70
HUMEDAD_MINIMA = 40
HUMEDAD_MAXIMA = 65

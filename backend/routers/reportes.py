from datetime import date

from fastapi import APIRouter, Depends, Query

from core.errores import ReglaNegocio
from routers.dependencias import RESPUESTAS_COMUNES, usuario_actual
from services import dashboard_service, reportes_service

router = APIRouter(prefix="/api", tags=["Dashboard y reportes"], responses=RESPUESTAS_COMUNES)


@router.get("/dashboard", summary="Indicadores del dashboard")
def dashboard(_: dict = Depends(usuario_actual)):
    """Toneladas desviadas de vertederos, kilos de abono producido, rendimiento,
    gráficos por mes, por tipo de residuo y por fase, y alertas de pilas activas."""
    return dashboard_service.obtener()


@router.get("/reportes/mensual", summary="Consolidado mensual de toneladas transformadas")
def reporte_mensual(
    anio: int | None = Query(None, ge=2000, le=2100, description="Por defecto, el año actual"),
    _: dict = Depends(usuario_actual),
):
    return reportes_service.consolidado_mensual(anio or date.today().year)


@router.get("/reportes/proveedores", summary="Consolidado de residuo aportado por proveedor")
def reporte_proveedores(fecha_desde: date, fecha_hasta: date, _: dict = Depends(usuario_actual)):
    if fecha_hasta < fecha_desde:
        raise ReglaNegocio("La fecha final no puede ser anterior a la fecha inicial")
    return reportes_service.por_proveedor(fecha_desde, fecha_hasta)


@router.get("/reportes/anios", summary="Años con información disponible")
def anios(_: dict = Depends(usuario_actual)):
    return reportes_service.anios_disponibles()

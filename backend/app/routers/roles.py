from fastapi import APIRouter, HTTPException
from app.database.connection import fetch_ords

router = APIRouter(
    prefix="/api/roles",
    tags=["Roles"]
)

@router.get("/", summary="Obtener todos los roles")
def get_roles():
    try:
        data = fetch_ords("roles")
        # ORDS devuelve un diccionario con la clave 'items'
        return {"data": data.get("items", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter

router = APIRouter(prefix="/materiales", tags=["Materiales"])

@router.get("/")
def obtener_materiales():
    return {"message": "Aquí se mostrarán los materiales disponibles."}
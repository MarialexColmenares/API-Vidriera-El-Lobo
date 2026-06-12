from fastapi import APIRouter, Depends
from sqlmodel import Session
from database.conexion import get_db
from services.abonos_services import * 
from schemas.esquemas import AbonosResponse, AbonoCreate

router = APIRouter(prefix="/abonos", tags=["Abonos"])

@router.get("/")
def obtener_abonos(session: Session = Depends(get_db)):
    return obtener_abonos_service(session)

@router.post("/", status_code=201, response_model=AbonosResponse)
def crear_abono(data: AbonoCreate, session: Session = Depends(get_db)):
    return crear_abono_service(data=data, session=session)

@router.get("/{id_abono}", response_model=AbonosResponse)
def obtener_abono_id(id_abono: int, session: Session = Depends(get_db) ):
    return obtener_abono_id_service(id_abono=id_abono, session=session)

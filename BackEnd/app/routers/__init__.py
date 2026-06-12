# Este archivo se encarga de centralizar la importación de todos los routers y luego exportarlos como un solo router para ser incluido en el main.py

from fastapi import APIRouter
from routers.material_router import router as material_router
from routers.permisos_router import router as permisos_router
from routers.preguntas_seguridad_router import router as preguntas_seguridad_router
from routers.roles_router import router as roles_router
from routers.usuarios_router import router as usuarios_router
from routers.ordenes_trabajo_router import router as ordenes_trabajo_router
from routers.abonos_router import router as abonos_router

router_central = APIRouter()

# Incluimos cada sub-router en nuestro router central
router_central.include_router(roles_router)
router_central.include_router(permisos_router)
router_central.include_router(usuarios_router)
router_central.include_router(preguntas_seguridad_router)
router_central.include_router(material_router)
router_central.include_router(ordenes_trabajo_router)
router_central.include_router(abonos_router)
from datetime import date

from pydantic import BaseModel, Field

class PreguntasSegurdadCreate(BaseModel):
    pregunta: str
    class Config:
        from_attributes = True  
        
        json_schema_extra = {
            "example": {
                "pregunta": "¿Cuál fue el nombre de tu primera mascota?"
            }
        }
        
class RolCreate(BaseModel):
    nombre_rol: str
    descripcion: str
    class Config:
        json_schema_extra = {
            "example": {
                "nombre_rol": "cliente",
                "descripcion": "Rol para usuarios clientes"
            }
        }

class PermisoCreate(BaseModel):
    nombre: str
    descripcion: str
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Crear: ordenes",
                "descripcion": "Permiso para crear ordenes de trabajo"
            }
        }

class usuarioCreate(BaseModel):
    nombre: str
    apellido: str
    correo: str
    password: str
    documento: str 
    rol_id: int
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Crear: ordenes",
                "apellido": "Permiso para crear ordenes de trabajo",
                "correo": "persona@examplo.com",
                "password": "contraseña123",
                "documento": "123456789",
                "rol_id": 1
            }
        }
        
# nuevo esquema para leer usuarios 
class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    correo: str
    documento: str
    rol_id: int

    class Config:
        from_attributes = True  # En Pydantic v2 (antiguo orm_mode = True) para leer objetos de SQLModel/SQLAlchemy
        
class UsuarioRespuestaSeguridadCreate(BaseModel):
    pregunta_id: int = Field(..., description="El ID de la pregunta predefinida en el catálogo")
    respuesta: str = Field(..., min_length=2, max_length=255, description="La respuesta escrita por el usuario")

    class Config:
        json_schema_extra = {
            "example": {
                "pregunta_id": 1,
                "respuesta": "Mi primer perrito Firulais"
            }
        }
        
class UsuarioRespuestaSeguridadResponse(BaseModel):
    id: int
    usuario_id: int
    pregunta_id: int

    class Config:
        from_attributes = True  # En Pydantic v2 (antiguo orm_mode = True) para leer objetos de SQLModel/SQLAlchemy
        
        
class MaterialCreate(BaseModel):
    nombre: str 
    espesor_mm: float
    color: str
    stock_disponible: float  # estaba dudando si poner cantidad aqui o en un almacen de stock, pero creo que es mejor ponerlo aqui para tener un control de la cantidad total de cada material, y luego en el stock solo se restaria la cantidad utilizada en cada orden de trabajo, asi se mantiene un historial de los materiales utilizados en cada orden de trabajo y no se pierde informacion al eliminar materiales del stock. Ademas, si se necesita agregar mas materiales en el futuro, solo se tendria que crear un nuevo registro en esta tabla sin afectar el historial de los materiales utilizados en las ordenes de trabajo anteriores.
    precio_m2: float
    
    

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Tornillo M8",
                "espesor_mm": 8.0,
                "color": "Plateado",
                "stock_disponible": 100.0,
                "precio_m2": 10.0
            }
        }

class MaterialUpdate(BaseModel):
    id: int
    cantidad_a_sumar: float

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "cantidad_a_sumar": 50.0
            }
        }


# orden trabajo

# 1. Esquema para recibir cada vidrio/ítem individual de la orden
class OrdenDetalleCreate(BaseModel):
    descripcion: str       # Ej: "Vidrio templado para ventana"
    material_id: int       # ID del tipo de vidrio en almacén
    ancho_m: float         # Medidas en metros
    alto_m: float
    cantidad: int

# 2. Esquema principal que recibirá el endpoint POST /ordenes
class OrdenTrabajoCreate(BaseModel):
    cliente_id: int
    fecha_entrega_estimado: date
    detalles: list[OrdenDetalleCreate] # <--- La lista con todos los vidrios de la orden

    class Config:
        # Esto te genera un ejemplo limpio en el Swagger UI de FastAPI
        json_schema_extra = {
            "example": {
                "cliente_id": 1,
                "fecha_entrega_estimado": "2026-06-15",
                "detalles": [
                    {
                        "descripcion": "Ventanal principal panorámico",
                        "material_id": 2,
                        "ancho_m": 2.10,
                        "alto_m": 1.50,
                        "cantidad": 1
                    },
                    {
                        "descripcion": "Puerta de baño esmerilada",
                        "material_id": 4,
                        "ancho_m": 0.80,
                        "alto_m": 1.90,
                        "cantidad": 2
                    }
                    ]
                }
            }
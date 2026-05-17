from typing import Optional, List
from datetime import datetime, date 
from sqlmodel import Field, SQLModel, Relationship

class Roles_Permisos(SQLModel, table=True):
    __tablename__: str = "roles_permisos"
    
    rol_id: int = Field(foreign_key="roles.id", primary_key=True)
    permiso_id: int = Field(foreign_key="permisos.id", primary_key=True)

class Permisos(SQLModel, table=True):
    __tablename__: str = "permisos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, index=True)
    descripcion: str

    roles: List["Rol"] = Relationship(back_populates="permisos", link_model=Roles_Permisos)

class Rol(SQLModel, table=True):
    __tablename__: str = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_rol: str = Field(unique=True, index=True)
    descripcion: str
    
    usuarios: List["Usuarios"] = Relationship(back_populates="rol")
    permisos: List[Permisos] = Relationship(back_populates="roles", link_model=Roles_Permisos)

class material(SQLModel, table=True):
    __tablename__: str = "material"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, index=True)
    espesor_mm: float
    color: str
    stock_disponible: float
    precio_m2: float

class PreguntasSeguridad(SQLModel, table=True):
    __tablename__: str = "Preguntas_seguridad"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    pregunta: str
    respuesta: str
    
    usuario: Optional["Usuarios"] = Relationship(back_populates="preguntas_seguridad")

class Usuarios(SQLModel, table=True):
    __tablename__: str = "usuarios"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    correo: str = Field(unique=True, index=True)
    password: str
    documento: str = Field(unique=True, index=True)
    telefono: str
    rol_id: int = Field(foreign_key="roles.id")
    
    rol: Optional[Rol] = Relationship(back_populates="usuarios")
    preguntas_seguridad: List[PreguntasSeguridad] = Relationship(back_populates="usuario")

class ordenes_trabajo(SQLModel, table=True):
    __tablename__: str = "orden"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    codigo_orden: str = Field(unique=True, index=True)
    cliente_id: Optional[int] = Field(foreign_key="usuarios.id")
    fecha_entrega_estimado: date 
    estado: Optional[str] = Field(default="Pendiente") 
    monto_total: Optional[float] = Field(default=None)


class orden_detalle(SQLModel, table=True):
    __tablename__: str = "detalles_de_orden"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str
    orden_id: int = Field(foreign_key="orden.id")  
    material_id: int = Field(foreign_key="material.id")
    ancho_m: float
    alto_m: float
    cantidad: int

class trazabilidad(SQLModel, table=True):
    __tablename__: str = "trazabilidad"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    orden_id: int = Field(foreign_key="orden.id")  
    etapa: str
    operador_id: Optional[int] = Field(foreign_key="usuarios.id")
    autorizado_por: Optional[int] = Field(foreign_key="usuarios.id")
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = Field(default=None)
    observaciones: Optional[str] = Field(default=None)
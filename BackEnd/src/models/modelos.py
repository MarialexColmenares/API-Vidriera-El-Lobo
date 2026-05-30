from typing import Optional, List
from datetime import datetime, date 
from sqlmodel import Field, SQLModel, Relationship
class Rol_Permiso(SQLModel, table=True):
    __tablename__: str = "roles_permisos"
    
    rol_id: int = Field(foreign_key="roles.id", primary_key=True)
    permiso_id: int = Field(foreign_key="permisos.id", primary_key=True)
class Permiso(SQLModel, table=True):
    __tablename__: str = "permisos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, index=True)
    descripcion: str
    roles: List["Rol"] = Relationship(back_populates="permisos", link_model=Rol_Permiso)

class Rol(SQLModel, table=True):
    __tablename__: str = "roles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_rol: str = Field(unique=True, index=True)
    descripcion: str
    
    usuarios: List["Usuario"] = Relationship(back_populates="rol")
    permisos: List[Permiso] = Relationship(back_populates="roles", link_model=Rol_Permiso)

class PreguntaSeguridad(SQLModel, table=True):
    __tablename__: str = "preguntas_seguridad"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    pregunta: str
    
    respuestas: List["UsuarioRespuestaSeguridad"] = Relationship(back_populates="pregunta")
class UsuarioRespuestaSeguridad(SQLModel, table=True):
    __tablename__: str = "usuario_respuestas_seguridad"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id")
    pregunta_id: int = Field(foreign_key="preguntas_seguridad.id")
    respuesta: str 

    usuario: Optional["Usuario"] = Relationship(back_populates="respuestas_seguridad")
    pregunta: Optional[PreguntaSeguridad] = Relationship(back_populates="respuestas")
class Usuario(SQLModel, table=True):
    __tablename__: str = "usuarios"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    correo: str = Field(unique=True, index=True)
    password: str
    documento: str = Field(unique=True, index=True)
    rol_id: int = Field(foreign_key="roles.id")
    
    rol: Optional[Rol] = Relationship(back_populates="usuarios")
    respuestas_seguridad: List[UsuarioRespuestaSeguridad] = Relationship(back_populates="usuario")
    ordenes: List["OrdenTrabajo"] = Relationship(back_populates="cliente")

class Material(SQLModel, table=True):
    __tablename__: str = "material"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, index=True)
    espesor_mm: float
    color: str
    stock_disponible: float
    precio_m2: float
class OrdenTrabajo(SQLModel, table=True):
    __tablename__: str = "orden"
    id: Optional[int] = Field(default=None, primary_key=True)
    codigo_orden: str = Field(unique=True, index=True)
    cliente_id: Optional[int] = Field(foreign_key="usuarios.id")
    fecha_entrega_estimado: date 
    estado: Optional[str] = Field(default="Pendiente") 
    monto_total: Optional[float] = Field(default=None)
    estado_pago: str = Field(default="Pendiente") 

    cliente: Optional[Usuario] = Relationship(back_populates="ordenes")
    abonos: List["Abono"] = Relationship(back_populates="orden")
class OrdenDetalle(SQLModel, table=True):
    __tablename__: str = "detalles_de_orden"
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str
    orden_id: int = Field(foreign_key="orden.id")  
    material_id: int = Field(foreign_key="material.id")
    ancho_m: float
    alto_m: float
    cantidad: int

class Abono(SQLModel, table=True):
    __tablename__: str = "abonos"
    id: Optional[int] = Field(default=None, primary_key=True)
    monto: float = Field(default=0.0)
    fecha_pago: datetime = Field(default_factory=datetime.utcnow)
    metodo_pago: str  
    observaciones: Optional[str] = Field(default=None)
    orden_id: int = Field(foreign_key="orden.id")

    orden: Optional["OrdenTrabajo"] = Relationship(back_populates="abonos")
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
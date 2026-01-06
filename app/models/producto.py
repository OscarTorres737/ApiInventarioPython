from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Producto(BaseModel):
    id_producto: int
    nombre: str
    descripcion: str
    precio: float
    stock: int
    id_categoria: int
    id_proveedor: int
    fecha_alta: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
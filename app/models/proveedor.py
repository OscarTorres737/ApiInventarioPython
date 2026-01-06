from pydantic import BaseModel

class Proveedor(BaseModel):
    id_proveedor: int
    nombre: str
    direccion: str
    rfc: str

    class Config:
        from_attributes = True
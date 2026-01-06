from pydantic import BaseModel

class Categoria(BaseModel):
    id_categoria: int
    nombre_categoria: str

    class Config:
        from_attributes = True # Esto permite convertir objetos SQL a objetos Pydantic automáticamente
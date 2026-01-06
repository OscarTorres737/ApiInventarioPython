from typing import List
from fastapi import APIRouter, HTTPException
import pyodbc
from app.database import get_connection
from app.models.categoria import Categoria

router = APIRouter()

#get categorias
@router.get("/categorias", response_model=List[Categoria])
def get_categorias():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC SP_ObtenerCategorias")
        rows = cursor.fetchall()

        categorias = []
        for row in rows:
            categorias.append(Categoria(id_categoria=row[0], nombre_categoria=row[1]))
        return categorias
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

#get categorias por id
@router.get("/categorias/{id_categoria}", response_model=List[Categoria])
def get_categoriasid(id_categoria:int):
    conn = get_connection()
    cursor = conn.cursor()

    try: 
        #llamamos al sp de obtener categorias
        cursor.execute("EXEC SP_ObtenerCategoriasPorId @IdCategoria=?", (id_categoria))
        rows = cursor.fetchall()

        categorias = []
        for row in rows:
            categorias.append(Categoria(id_categoria=row[0], nombre_categoria=row[1]))
        return categorias
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

#post categorias
@router.post("/categorias")
def post_categorias(nombre_categoria:str):
    conn = get_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("EXEC SP_InsertCategoria @NombreCategoria=?", (nombre_categoria))
        
        #recuperamos mensaje que arroja el sp
        row = cursor.nextset()

        conn.commit()

        return {"mensaje": row[0] if row else "Categoría creada", "data": row}
    
    except pyodbc.Error as e:
        error_msg = str(e.args[1]) if len(e.args) > 1 else str(e)
        if "50001" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        else:
            raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        cursor.close()
        conn.close()

#put categoria
@router.put("/categorias/{id_categoria}")
def update_categorias(id_categoria: int, nombre_categoria: str):
    conn = get_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("EXEC SP_UpdateCategoria @IdCategoria=?, @NombreCategoria=?", (id_categoria, nombre_categoria))
        
        #recuperamos mensaje que arroja el sp
        row = cursor.fetchone()

        conn.commit()

        return {"mensaje": row[0] if row else "Categoría actualizada"}
    
    except pyodbc.Error as e:
        error_msg = str(e.args[1]) if len(e.args) > 1 else str(e)
        if "50002" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        else:
            raise HTTPException(status_code=500, detail="Error al actualizar")
    finally:
        cursor.close()
        conn.close()

#delete categoria
@router.delete("/categorias/{id_categoria}")
def delete_categorias(id_categoria: int):
    conn = get_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("EXEC SP_DeleteCategoria @IdCategoria=?", (id_categoria))
        
        #recuperamos mensaje que arroja el sp
        row = cursor.fetchone()

        conn.commit()

        return {"mensaje": row[0] if row else "Categoría eliminada"}
    
    except pyodbc.Error as e:
        error_msg = str(e.args[1]) if len(e.args) > 1 else str(e)
        if "50003" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        else:
            raise HTTPException(status_code=500, detail="Error al eliminar")
    finally:
        cursor.close()
        conn.close()


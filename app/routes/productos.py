from typing import List
import pyodbc
from fastapi import APIRouter, HTTPException
from app.database import get_connection
from app.models.producto import Producto


router = APIRouter()

#get productos
@router.get("/productos", response_model=List[Producto])
def get_productos():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC SP_ObtenerProductos")
        rows = cursor.fetchall()

        productos = []
        for row in rows:
            productos.append(Producto(id_producto=row[0], nombre=row[1], descripcion=row[2], precio=row[3], stock=row[4], id_proveedor=row[5], id_categoria=row[6], fecha_alta=row[7], fecha_actualizacion=row[8]))
        return productos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

#get productos por id
@router.get("/productos/{id_producto}", response_model=List[Producto])
def get_productosid(id_producto:int):
    conn = get_connection()
    cursor = conn.cursor()

    try: 
        #llamamos al sp de obtener productos
        cursor.execute("EXEC SP_ObtenerProductosPorId @IdProducto=?", (id_producto))
        rows = cursor.fetchall()

        productos = []
        for row in rows:
            productos.append(Producto(id_producto=row[0], nombre=row[1], descripcion=row[2], precio=row[3], stock=row[4], id_proveedor=row[5], id_categoria=row[6], fecha_alta=row[7], fecha_actualizacion=row[8]))
        return productos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

#post producto
@router.post("/productos")
def post_productos(nombre:str, descripcion:str, precio:float, stock:int, id_categoria:int, id_proveedor:int):
    conn = get_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("EXEC SP_InsertProducto @Nombre=?, @Descripcion=?, @Precio=?, @Stock=?, @IdCategoria=?, @IdProveedor=?", (nombre, descripcion, precio, stock, id_categoria, id_proveedor))
        
        #recuperamos mensaje que arroja el sp
        row = cursor.nextset()

        conn.commit()

        return {"mensaje": row[0] if row else "Producto creada", "data": row}
    
    except pyodbc.Error as e:
        error_msg = str(e.args[1]) if len(e.args) > 1 else str(e)
        if "50004" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        else:
            raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        cursor.close()
        conn.close()

#put producto
@router.put("/productos/{id_producto}")
def update_producto(id_producto: int, nombre:str, descripcion:str, precio:float, stock:int):
    conn = get_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("EXEC SP_UpdateProducto @IdProducto=?, @Nombre=?, @Descripcion=?, @Precio=?, @Stock=?", (id_producto,nombre, descripcion, precio, stock))
        
        #recuperamos mensaje que arroja el sp
        row = cursor.fetchone()

        conn.commit()

        return {"mensaje": row[0] if row else "Producto actualizado"}
    
    except pyodbc.Error as e:
        error_msg = str(e.args[1]) if len(e.args) > 1 else str(e)
        if "50005" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        else:
            raise HTTPException(status_code=500, detail="Error al actualizar")
    finally:
        cursor.close()
        conn.close()

#delete producto
@router.delete("/productos/{id_producto}")
def delete_producto(id_producto: int):
    conn = get_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("EXEC SP_DeleteProducto @IdProducto=?", (id_producto))
        
        #recuperamos mensaje que arroja el sp
        row = cursor.fetchone()

        conn.commit()

        return {"mensaje": row[0] if row else "Producto eliminado"}
    
    except pyodbc.Error as e:
        error_msg = str(e.args[1]) if len(e.args) > 1 else str(e)
        if "50006" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        else:
            raise HTTPException(status_code=500, detail="Error al eliminar")
    finally:
        cursor.close()
        conn.close()
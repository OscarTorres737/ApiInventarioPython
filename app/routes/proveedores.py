from typing import List
from fastapi import APIRouter, HTTPException
import pyodbc
from app.database import get_connection
from app.models.proveedor import Proveedor


router = APIRouter()

#get productos
@router.get("/proveedores", response_model=List[Proveedor])
def get_proveedores():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC SP_ObtenerProveedores")
        rows = cursor.fetchall()

        proveedores = []
        for row in rows:
            proveedores.append(Proveedor(id_proveedor=row[0], nombre=row[1], direccion=row[2], rfc=row[3]))
        return proveedores
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

#get proveedor por id
@router.get("/proveedores/{id_proveedor}", response_model=List[Proveedor])
def get_proveedoresid(id_proveedor:int):
    conn = get_connection()
    cursor = conn.cursor()

    try: 
        #llamamos al sp de obtener proveedor
        cursor.execute("EXEC SP_ObtenerProveedoresPorId @IdProveedor=?", (id_proveedor))
        rows = cursor.fetchall()

        proveedores = []
        for row in rows:
            proveedores.append(Proveedor(id_proveedor=row[0], nombre=row[1], direccion=row[2], rfc=row[3]))
        return proveedores
    except pyodbc.Error as e:
        error_msg = str(e.args[1]) if len(e.args) > 1 else str(e)
        if "50007" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        else:
            raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        cursor.close()
        conn.close()

#post proveedor
@router.post("/proveedores")
def post_proveedor(nombre:str, direccion:str, rfc:str):
    conn = get_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("EXEC SP_InsertProveedor @Nombre=?, @Direccion=?, @RFC=?", (nombre, direccion, rfc))
        
        #recuperamos mensaje que arroja el sp
        row = cursor.nextset()

        conn.commit()

        return {"mensaje": row[0] if row else "Proveedor registrado", "data": row}
    
    except pyodbc.Error as e:
        error_msg = str(e.args[1]) if len(e.args) > 1 else str(e)
        if "50008" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        else:
            raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        cursor.close()
        conn.close()

#put proveedor
@router.put("/proveedor/{id_proveedor}")
def update_proveedor(id_proveedor:int, nombre:str, direccion:str):
    conn = get_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("EXEC SP_UpdateProveedor @IdProveedor=?, @Nombre=?, @Direccion=?", (id_proveedor, nombre, direccion))
        
        #recuperamos mensaje que arroja el sp
        row = cursor.fetchone()

        conn.commit()

        return {"mensaje": row[0] if row else "Proveedor actualizado"}
    
    except pyodbc.Error as e:
        error_msg = str(e.args[1]) if len(e.args) > 1 else str(e)
        if "50009" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        else:
            raise HTTPException(status_code=500, detail="Error al actualizar")
    finally:
        cursor.close()
        conn.close()

#delete proveedor
@router.delete("/proveedor/{id_proveedor}")
def delete_proveedor(id_proveedor: int):
    conn = get_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("EXEC SP_DeleteProveedor @IdProveedor=?", (id_proveedor))
        
        #recuperamos mensaje que arroja el sp
        row = cursor.fetchone()

        conn.commit()

        return {"mensaje": row[0] if row else "Proveedor eliminado"}
    
    except pyodbc.Error as e:
        error_msg = str(e.args[1]) if len(e.args) > 1 else str(e)
        if "500010" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        else:
            raise HTTPException(status_code=500, detail="Error al eliminar")
    finally:
        cursor.close()
        conn.close()
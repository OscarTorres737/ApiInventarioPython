from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import categorias, proveedores
from app.routes import productos


#iniciaos la aplicacion
app = FastAPI(title="Api de Inventario", version="1.0.0")

app.include_router(categorias.router)
app.include_router(productos.router)
app.include_router(proveedores.router)

#configuramos cors para que aplicaciones de react o vue puedan usar la api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

#ruta de prueba para saber que el server está vivo
@app.get("/")
def root():
    return {"mensaje": "Api de inventarios correindo bien"}
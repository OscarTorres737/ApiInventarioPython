# Inventarios API (Python + SQL Server)

API REST sencilla para **control de inventarios**: CRUD básico de **Productos**, **Categorías** y **Proveedores**.

La API se conecta a **SQL Server** y, en lugar de meter la lógica en el backend, **solo ejecuta Stored Procedures (SPs)**.  
Toda la lógica de negocio, validaciones y reglas (incluyendo errores controlados) viven en la base de datos.

> Nota personal: es de las primeras veces que trabajo una API completa en **Python**. Aun así, este proyecto me sirvió para demostrar que puedo **adaptarme a tecnologías nuevas** y aportar valor rápido en un desarrollo, cuidando estructura, claridad y resultados.

---

## 🧱 Stack

- **Python** (API)
- **SQL Server** (DB)
- **Stored Procedures** para toda la lógica (insert/update/delete/get)
- **pyodbc** para conexión
- Variables de entorno con **.env**

---

## ✅ Requisitos

- Python 3.10+ (recomendado)
- SQL Server (local o remoto)
- ODBC Driver 17 para SQL Server

---

## ⚙️ Configuración

### 1) Clonar y preparar entorno
```bash
git clone https://github.com/OscarTorres737/ApiInventarioPython.git
cd ApiInventarioPython

python -m venv .venv
# Windows
.\.venv\Scripts\activate

````

### 2) Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🔐 Variables de entorno

Crea un archivo `.env` en la raíz del proyecto.

Ejemplo:

```env
DB_CONNECTION_STRING=Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=InventariosDb;Trusted_Connection=yes;TrustServerCertificate=yes;
```

Si usas usuario/contraseña:

```env
DB_CONNECTION_STRING=Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=InventariosDb;Uid=sa;Pwd=TuPassword;TrustServerCertificate=yes;
```

---

## 🗄️ Base de datos (SQL Server)

Ejecuta el compilado que esta adjunto a este repositorio para crear la base de datos con sus respectivas tablas y con datos demo.

---

## 🚀 Correr la API

### Con FastAPI
```bash
uvicorn app.main:app --reload
```

---

## 🧠 Lógica en Stored Procedures

La API **no hace validaciones complejas** en el backend: solo manda parámetros a los SPs y devuelve la respuesta.

Ventajas de este enfoque:

* Reglas y validaciones centralizadas en SQL Server
* La API queda limpia y fácil de mantener
* Validaciones consistentes sin duplicar lógica

---

## 🧩 Códigos de error personalizados (THROW)

Los SPs manejan errores controlados usando la **instrucción** `THROW`, con:

* **Número de error** (>= 50000) para identificar el tipo de error
* **State** para diferenciar casos/variantes

Ejemplo (idea general):

* `50001` → validación de categoría

  * state `1` → nombre null
  * state `2` → longitud inválida
  * state `3` → duplicado

Esto ayuda a que desde la API pueda traducir errores a respuestas claras (por ejemplo `400 Bad Request`) sin perder el detalle de lo que falló.

---

## 👤 Autor

Proyecto desarrollado por **Oscar Torres**.

Aunque Python no es el lenguaje que más he usado, este proyecto refleja algo importante para mí: puedo **adaptarme rápido**, entender el flujo completo (API + DB), y entregar una solución funcional con buenas prácticas y un enfoque claro.

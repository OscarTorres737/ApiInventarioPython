import os
import pyodbc
from dotenv import load_dotenv


load_dotenv() 

def get_connection():

    connection_string = os.getenv("DB_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("Falta DB_CONNECTION_STRING en el .env o en las variables de entorno.")
    
    return pyodbc.connect(connection_string)
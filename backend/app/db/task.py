#Se usa para establecerá nuestra conexión a la base de datos y se encargará de cualquier configuración adicional que necesitemos
import os
from fastapi import FastAPI
from databases import Database
from app.core.config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

async def connect_to_db(app: FastAPI) -> None:
    #Verifica si el ambiente es de prueba para crear la DB de prueba
    DB_URL = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else DATABASE_URL
    database = Database(DB_URL, min_size=2, max_size=10)

    try:
        await database.connect()
        app.state._db = database
        logger.warning("--- DB CONNECT ---")

    except Exception as e:
        logger.warning("--- DB CONNECTION ERROR ---")
        logger.warning(e)
        logger.warning("--- DB CONNECTION ERROR ---")

async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
        logger.warning("--- DB DISCONNECT ---")
        
    except Exception as e:
        logger.warning("--- DB DISCONNECT ERROR ---")
        logger.warning(e)
        logger.warning("--- DB DISCONNECT ERROR ---")
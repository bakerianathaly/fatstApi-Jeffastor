#Se usa para establecerá nuestra conexión a la base de datos y se encargará de cualquier configuración adicional que necesitemos

from fastapi import FastAPI
from databases import Database
from app.core.config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

async def connect_to_db(app: FastAPI) -> None:
    database = Database(DATABASE_URL, min_size=2, max_size=10)  # these can be configured in config as well
    try:
        await database.connect()
        app.state._db = database
        logger.warn("--- DB CONNECT ---")

    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")

async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
        logger.warn("--- DB DISCONNECT ---")
        
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")
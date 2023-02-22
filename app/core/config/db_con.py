from pymongo import MongoClient
from core.config.config import settings

conn = MongoClient(settings.RUTA_MONGO)

db_ecom = conn.ecommerce
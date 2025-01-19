import os
import time

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()



class Config:
    LOGGER = True
    STRING_SESSION = os.environ.get("STRING_SESSION")
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    DATABASE_URI = os.environ.get("DATABASE_URI")
    DATABASENAME = os.environ.get("DATABASENAME")
    VERSION = os.environ.get("VERSION")
    WORKERS = int(os.environ.get("WORKERS", 16))
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL"))
    SUDO_USERS=os.environ.get("SUDO_USERS")
    PREFIX_HANDLER = os.environ.get("PREFIX_HANDLER", "/").split()
    SUPPORT_GROUP = os.environ.get("SUPPORT_GROUP")
    SUPPORT_CHANNEL = os.environ.get("SUPPORT_CHANNEL")
    BOT_TOKEN=os.environ.get("BOT_TOKEN")
    PROMOTION_NAME=os.environ.get('PROMOTION_NAME')
    WEBHOOK=os.environ.get('WEBHOOK')
    BOT_UPTIME  = time.time()
    START_PIC = os.environ.get("START_PIC")
    
def check_mongodb_connection():
    try:
        client = MongoClient(Config.DATABASE_URI)
        client.admin.command('ismaster')
        print("MongoDB connection: Successful")
    except Exception as e:
        print(f"MongoDB connection: Failed - {e}")

check_mongodb_connection() 

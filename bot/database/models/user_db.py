from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from datetime import datetime
import threading
from bot import LOGGER, DATABASENAME, DATABASE_URI

client = AsyncIOMotorClient(DATABASE_URI)  
db = client[DATABASENAME]
users_collection = db['users']
admins_collection = db['admins']

sync_client = MongoClient(DATABASE_URI)  
sync_db = sync_client[DATABASENAME]
sync_admins_collection = sync_db['admins']

LOCK = threading.RLock()

async def add_user(message):
    first_name = message.from_user.first_name or 'None'
    last_name = message.from_user.last_name or 'None'
    username = message.from_user.username or 'None'
    chat_id = message.chat.id

    with LOCK:
        user = await users_collection.find_one({"chat_id": chat_id})
        if not user:
            await users_collection.insert_one({
                "chat_id": chat_id,
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "date": datetime.now()  
            })
            # LOGGER.info(f'New User : chat_id {chat_id} username {username}')
        else:
            await users_collection.update_one(
                {"chat_id": chat_id},
                {"$set": {"first_name": first_name, "last_name": last_name, "username": username}}
            )

async def delete_user(chat_id):
    with LOCK:
        await users_collection.delete_one({"chat_id": chat_id})

def get_admin():
    admins = sync_admins_collection.find()
    return [admin['chat_id'] for admin in admins]

async def get_all():
    users = await users_collection.find().to_list(None)  
    return [user['chat_id'] for user in users]

def add_admin(chat_id):
    with LOCK:
        admin = sync_admins_collection.find_one({"chat_id": chat_id})
        if not admin:
           sync_admins_collection.insert_one({"chat_id": int(chat_id)})
            # LOGGER.info(f'Admin ajouté : chat_id {chat_id}')
        else:
            # LOGGER.info(f'L\'admin existe déjà : chat_id {chat_id}')
            pass

async def total_users():
    return await users_collection.count_documents({})

async def total_admin():
    return await admins_collection.count_documents({})

async def get_all_user_data():
    cursor = users_collection.find()
    users = await cursor.to_list(None)
    return users

async def get_user_username(chat_id):
    user = await users_collection.find_one({"chat_id": chat_id})
    return user['username'] if user else None

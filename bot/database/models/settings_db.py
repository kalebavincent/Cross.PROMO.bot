from pymongo import MongoClient
from threading import RLock
from datetime import datetime

from bot import LOGGER, DATABASENAME, DATABASE_URI


client = MongoClient(DATABASE_URI)
db = client[DATABASENAME]
settings_collection = db['settings']
LOCK = RLock()

def initialize_settings():
    with LOCK:
        settings = settings_collection.find_one({"id": 1})
        if not settings:
            settings_collection.insert_one({
                "id": 1,
                "subs_limit": 0,   
                "list_size": 25,
                "grid_size": 3,
                "created_at": datetime.now()
            })
            print("Paramètres par défaut ajoutés.")

initialize_settings()


def add_subs_limit(limit):
    with LOCK:
        settings_collection.update_one(
            {"id": 1},
            {"$set": {"subs_limit": int(limit)}}
        )
        print(f"Limite des abonnés mise à jour : {limit}")

def add_list_size(size):
    with LOCK:
        settings_collection.update_one(
            {"id": 1},
            {"$set": {"list_size": int(size)}}
        )
        print(f"Taille de la liste mise à jour : {size}")

def add_grid_size(size):
    with LOCK:
        settings_collection.update_one(
            {"id": 1},
            {"$set": {"grid_size": int(size)}}
        )
        print(f"Taille de la grille mise à jour : {size}")

def get_settings():
    try:
        return settings_collection.find_one({"id": 1})
    finally:
        print("Lecture des paramètres terminée.")

def get_subcribers_limit():
    settings = settings_collection.find_one({"id": 1})
    if settings:
        return settings.get('subs_limit', 0)
    else:
        return 0

def get_list_size():
    settings = settings_collection.find_one({"id": 1})
    if settings:
        return settings.get('list_size', 25)
    else:
        return 25

def get_grid_size():
    settings = settings_collection.find_one({"id": 1})
    if settings:
        return settings.get('grid_size', 3)
    else:
        return 3

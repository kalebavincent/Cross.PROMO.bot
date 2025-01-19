from pymongo import MongoClient
from threading import RLock
from datetime import datetime

from config import Config

client = MongoClient(Config.DATABASE_URI)
db = client[Config.DATABASENAME]
promo_collection = db['promo']
paid_promo_collection = db['paid_promo']

LOCK = RLock()

def add_paidpromo(channel_id, message_id):
    with LOCK:
        paid_promo_collection.insert_one({
            "channel": int(channel_id),
            "message_id": int(message_id),
            "created_at": datetime.now()
        })
        print(f"PaidPromo ajouté : channel={channel_id}, message_id={message_id}")

def get_paidpromo():
    try:
        return list(paid_promo_collection.find())
    finally:
        print("Lecture des PaidPromo terminée.")

def delete_paid_promo():
    with LOCK:
        result = paid_promo_collection.delete_many({})
        print(f"{result.deleted_count} PaidPromo supprimés.")

def save_message_ids(channel_id, message_id):
    with LOCK:
        promo = promo_collection.find_one({"channel": int(channel_id)})
        if not promo:
            promo_collection.insert_one({
                "channel": int(channel_id),
                "message_id": int(message_id),
                "created_at": datetime.now()
            })
            print(f"Promo ajouté : channel={channel_id}, message_id={message_id}")
        else:
            promo_collection.update_one(
                {"channel": int(channel_id)},
                {"$set": {"message_id": int(message_id)}}
            )
            print(f"Promo mis à jour : channel={channel_id}, message_id={message_id}")

def get_promo():
    try:
        return list(promo_collection.find())
    finally:
        print("Lecture des Promo terminée.")

def delete_promo():
    with LOCK:
        result = promo_collection.delete_many({})
        print(f"{result.deleted_count} Promo supprimés.")


from pymongo import MongoClient
import threading
from datetime import datetime

from config import Config

client = MongoClient(Config.DATABASE_URI)
db = client[Config.DATABASENAME]
posts_collection = db['posts']
buttons_collection = db['buttons']

LOCK = threading.RLock()

def add_post(emoji=None, set_top=None, set_bottom=None, set_caption=None):
    with LOCK:
        # LOGGER.info(f"Received values - emoji: {emoji}, set_top: {set_top}, set_bottom: {set_bottom}, set_caption: {set_caption}")
        
        post = posts_collection.find_one({"_id": 1})
        
        if not post:
            # LOGGER.info("Adding new post")
            posts_collection.insert_one({
                "_id": 1,
                "emoji": emoji,
                "set_top": set_top,
                "set_bottom": set_bottom,
                "set_caption": set_caption,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            })
        else:
            update_needed = False
            update_fields = {}

            if emoji is not None and post["emoji"] != emoji:
                update_fields["emoji"] = emoji
                update_needed = True

            if set_top is not None and post["set_top"] != set_top:
                update_fields["set_top"] = set_top
                update_needed = True

            if set_bottom is not None and post["set_bottom"] != set_bottom:
                update_fields["set_bottom"] = set_bottom
                update_needed = True

            if set_caption is not None and post["set_caption"] != set_caption:
                update_fields["set_caption"] = set_caption
                update_needed = True

            if update_needed:
                update_fields["updated_at"] = datetime.now() 
                posts_collection.update_one(
                    {"_id": 1},
                    {"$set": update_fields}
                )
            else:
                # LOGGER.info("No changes detected, no update needed")
                pass

def add_emoji(emoji):
    # LOGGER.info(f"Adding emoji: {emoji}")
    add_post(emoji=emoji)

def add_caption(caption):
    # LOGGER.info(f"Adding caption: {caption}")
    add_post(set_caption=caption)

def add_top_text(text):
    # LOGGER.info(f"Adding top text: {text}")
    add_post(set_top=text)

def add_bottom_text(text):
    # LOGGER.info(f"Adding bottom text: {text}")
    add_post(set_bottom=text)

def get_post():
    return posts_collection.find_one({"_id": 1})

def add_button(name, url):
    with LOCK:
        buttons_collection.insert_one({
            "name": name,
            "url": url,
            "created_at": datetime.now()
        })

def delete_button():
    with LOCK:
        # LOGGER.info("Deleting all buttons")
        buttons_collection.delete_many({})

def get_buttons():
    return list(buttons_collection.find())

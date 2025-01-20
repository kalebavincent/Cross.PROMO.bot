from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

client = AsyncIOMotorClient(Config.DATABASE_URI)
db = client[Config.DATABASENAME]
channels_collection = db["channels"]
banned_collection = db["banned_channels"]

async def channel_data(chat_id, channel_id, channel_name, subscribers, admin_username, description, invite_link):
    # LOGGER.info(f"New Channel {channel_id} [{channel_name}] by {admin_username}")
    channel = {
        "chat_id": chat_id,
        "channel_id": int(channel_id),
        "channel_name": channel_name,
        "subscribers": subscribers,
        "admin_username": admin_username,
        "description": description,
        "invite_link": invite_link,
    }
    await channels_collection.update_one(
        {"channel_id": int(channel_id)},
        {"$set": channel},
        upsert=True
    )

async def is_channel_exist(channel_id):
    # LOGGER.info(f"Checking existence of {channel_id}")
    channel = await channels_collection.find_one({"channel_id": int(channel_id)})
    return channel is not None

async def is_channel_ban(channel_id):
    # LOGGER.info(f"Checking ban status for {channel_id}")
    banned = await banned_collection.find_one({"channel_id": int(channel_id)})
    return banned is not None

async def is_user_not_added_channel(chat_id):
    user_channel = await channels_collection.find_one({"chat_id": chat_id})
    return user_channel is None

async def delete_channel(channel_id):
    # LOGGER.info(f"Channel removed {channel_id}")
    await channels_collection.delete_one({"channel_id": int(channel_id)})

async def get_all_channel(chat_id):
    # LOGGER.info(f"Getting channels registered by {chat_id}")
    channels = channels_collection.find({"chat_id": chat_id})
    return [channel async for channel in channels]

async def get_channel():
    channels = channels_collection.find()
    return [channel async for channel in channels]

async def update_subs(channel_id, subs):
    await channels_collection.update_one(
        {"channel_id": int(channel_id)},
        {"$set": {"subscribers": subs}}
    )
async def total_channel():
    return await channels_collection.count_documents({})

async def total_banned_channel():
    return await banned_collection.count_documents({})

async def ban_channel(channel_id):
    await banned_collection.update_one(
        {"channel_id": int(channel_id)},
        {"$set": {"channel_id": int(channel_id)}},
        upsert=True
    )
    # LOGGER.info(f"Channel {channel_id} banned")

async def unban_channel(channel_id):
    await banned_collection.delete_one({"channel_id": int(channel_id)})

async def is_channel_banned(channel_id):
    banned = await banned_collection.find_one({"channel_id": int(channel_id)})
    return banned is not None

async def get_channel_by_id(channel_id):
    return await channels_collection.find_one({"channel_id": int(channel_id)})

async def get_banned_channel_list():
    banned_channels = banned_collection.find()
    return [channel["channel_id"] async for channel in banned_channels]

async def get_user_channel_count(chat_id):
    return await channels_collection.count_documents({"chat_id": chat_id})
        
async def chunck():
    channel_ids = []
    async for channel in channels_collection.find():
        channel_ids.append(channel["channel_id"])

    chunk_size = get_list_size()
    for i in range(0, len(channel_ids), chunk_size):
        yield channel_ids[i:i + chunk_size]

def get_list_size():
    return 100

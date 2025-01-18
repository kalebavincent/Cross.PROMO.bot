from pyrogram import filters, Client, enums
from pyrogram.types import Message
from bot import LOGGER, LOG_CHANNEL, SUDO_USERS, SUPPORT_GROUP
from bot.bot import Bot
from bot.utils.markup import channel_markup, start_markup
from motor.motor_asyncio import AsyncIOMotorClient
from bot import DATABASE_URI, DATABASENAME
from bot.database.models.channel_db import is_user_not_added_channel

client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASENAME]
channels_collection = db["channels"]

@Bot.on_callback_query(filters.regex('^my_channel$'))
async def my_channel_handler(bot: Client, message: Message):
    line = '_________________________________________________________'
    data = " "

    if not await is_user_not_added_channel(message.message.chat.id):
        await bot.send_message(
            message.message.chat.id,
            "⚠️ **Vous n'avez pas encore enregistré de canal avec notre bot ou les canaux peuvent avoir été supprimés ou bannis**",
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=start_markup()
        )
    else:
        channels = await channels_collection.find({"chat_id": message.message.chat.id}).to_list(length=None)

        total = await channels_collection.count_documents({"chat_id": message.message.chat.id})
        
        for channel in channels:
            data += f'{line}\nID du canal : {channel["channel_id"]}\nNom du canal : {channel["channel_name"]}\nAbonnés : {channel["subscribers"]}\n\n'

        await bot.send_message(
            message.message.chat.id,
            f'**Total des canaux : {total}**\n\n{data}',
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=channel_markup()
        )

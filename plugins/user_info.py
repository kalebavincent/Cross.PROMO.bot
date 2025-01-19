from pyrogram import filters, Client, enums
from pyrogram.types import Message
from config import Config
from motor.motor_asyncio import AsyncIOMotorClient
from utils.markup import channel_markup, start_markup
from database.models.channel_db import is_user_not_added_channel
import logging

LOG_CHANNEL = Config.LOG_CHANNEL
SUDO_USERS = Config.SUDO_USERS
SUPPORT_GROUP = Config.SUPPORT_GROUP
LOGGER = logging.getLogger(__name__)

client = AsyncIOMotorClient(Config.DATABASE_URI)
DATABASENAME = Config.DATABASENAME
db = client[DATABASENAME]
channels_collection = db["channels"]

@Client.on_callback_query(filters.regex('^my_channel$'))
async def my_channel_handler(bot: Client, message: Message):
    try:
        if await is_user_not_added_channel(message.message.chat.id):
            await bot.send_message(
                message.message.chat.id,
                "⚠️ **Vous n'avez pas encore enregistré de canal avec notre bot ou les canaux peuvent avoir été supprimés ou bannis.**",
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=start_markup()
            )
            return
        
        channels = await channels_collection.find({"chat_id": message.message.chat.id}).to_list(length=None)
        total = await channels_collection.count_documents({"chat_id": message.message.chat.id})

        if not channels:
            await bot.send_message(
                message.message.chat.id,
                "⚠️ **Aucun canal enregistré trouvé.**",
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=start_markup()
            )
            return

        for channel in channels:
            channel_id = channel["channel_id"]
            channel_name = channel["channel_name"]
            subscribers = channel.get("subscribers", "N/A")

            await bot.send_message(
                message.message.chat.id,
                (
                    f"**ID du canal :** `{channel_id}`\n"
                    f"**Nom du canal :** `{channel_name}`\n"
                    f"**Abonnés :** `{subscribers}`\n\n"
                ),
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=channel_markup()  
            )

        await bot.send_message(
            message.message.chat.id,
            f"**Total des canaux : {total}**",
            parse_mode=enums.ParseMode.MARKDOWN
        )

    except Exception as e:
        error_msg = f"Erreur inattendue dans `my_channel_handler` : {e}"
        LOGGER.error(error_msg, exc_info=True)
        await bot.send_message(
            LOG_CHANNEL,
            f"🚨 **Erreur dans `my_channel_handler`**\n\n<code>{error_msg}</code>",
            parse_mode=enums.ParseMode.HTML
        )
        await bot.send_message(
            message.message.chat.id,
            "❌ Une erreur s'est produite. Veuillez réessayer plus tard.",
            reply_markup=start_markup()
        )

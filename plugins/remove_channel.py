from pyrogram import filters, Client, enums
from pyrogram.types import Message
import traceback, time
from config import Config
LOG_CHANNEL = Config.LOG_CHANNEL
SUDO_USERS = Config.SUDO_USERS
SUPPORT_GROUP = Config.SUPPORT_GROUP
import logging
LOGGER = logging.getLogger(__name__)
from database.models.channel_db import delete_channel
from utils.markup import remove_channel_markup, start_markup

@Client.on_callback_query(filters.regex('remove_channel'))
async def remove_channel_message(bot: Client, message: Message):
    try:
        markup = await remove_channel_markup(message.from_user.id)
        
        await bot.edit_message_text(
            message.from_user.id,
            message.message.id,
            "Sélectionnez le canal à supprimer",
            reply_markup=markup
        )
    except Exception as e:
        await bot.send_message(LOG_CHANNEL, f"Erreur lors de l'édition du message : {str(e)}")
        LOGGER.error(f"Erreur lors de l'édition du message : {str(e)}")

@Client.on_callback_query(filters.regex(r'^-100\d+$')) 
async def remove_channel_handler(bot: Client, message: Message):
    try:
        channel_id = message.data
        await delete_channel(channel_id) 
        await bot.edit_message_text(
            message.from_user.id,
            message.message.id,
            "🗑 Canal supprimé avec succès.",
            reply_markup=start_markup()
        )
    except Exception as e:
        await bot.answer_callback_query(message.id, text="⚠️ Le canal n'existe pas", show_alert=True)
        error_message = f"Erreur de suppression du canal : {str(e)}"
        await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
        LOGGER.error(f"Erreur de suppression du canal : {str(e)}")

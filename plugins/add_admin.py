from pyrogram import filters, Client, enums
from pyrogram.types import Message
import traceback, time
from database.models.user_db import get_admin, add_admin
from utils.markup import admin_markup, back_markup, empty_markup
from config import Config
LOG_CHANNEL = Config.LOG_CHANNEL
import logging
LOGGER = logging.getLogger(__name__)


@Client.on_callback_query(filters.regex('^add_admin$') & filters.user(get_admin()))
async def add_admin_handler(bot: Client, message: Message):
    try:
        add_admins = await bot.ask(message.from_user.id, "Envoyez l'ID utilisateur Telegram de l'utilisateur\nNote : Il doit s'agir d'un utilisateur du bot", reply_markup=back_markup())
        if add_admins.text == '🚫 Cancel':
            await bot.send_message(message.from_user.id, 'Annulé', reply_markup=empty_markup())
        else:
            add_admin(int(add_admins.text))
            # LOGGER.info(f"{add_admins.text} ajouté en tant qu'administrateur par {message.from_user.id}")
            await bot.send_message(message.from_user.id, "Administrateur ajouté avec succès", reply_markup=empty_markup())
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
        await bot.send_message(message.from_user.id, 'Désolé :( , quelque chose a mal tourné', reply_markup=empty_markup())

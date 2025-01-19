from pyrogram import filters, Client, enums
from pyrogram.types import Message
import traceback, time
from database.models.user_db import get_all, get_admin
from utils.markup import start_markup, admin_markup, back_markup
from config import Config
LOG_CHANNEL = Config.LOG_CHANNEL
SUDO_USERS  = Config.SUDO_USERS
import logging
LOGGER = logging.getLogger(__name__)

@Client.on_callback_query(filters.regex('^mail$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def mail_handler(bot: Client, message: Message):
    mail_message = await bot.ask(message.from_user.id, 'Entrez le message', reply_markup=back_markup())
    
    if mail_message.text == '🚫 Annuler':
        await bot.send_message(message.from_user.id, "Envoi du message annulé", reply_markup=admin_markup())
        LOGGER.info("Envoi du message annulé")
    else:
        LOGGER.info("Envoi du message commencé")
        for user in get_all():
            try:
                await bot.send_message(user, mail_message.text)
                LOGGER.info(f"Envoi du message à {user}")
            except Exception as e:
                LOGGER.error(e)
                LOGGER.error(f"Message non envoyé à {user}")
                await bot.send_message(message.from_user.id, 'Désolé :( , Quelque chose s\'est mal passé', reply_markup=admin_markup())
                await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nHeure : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
                
        await bot.send_message(message.from_user.id, '☑️ Envoi du message terminé !', reply_markup=admin_markup())
        LOGGER.info('Envoi du message terminé !')

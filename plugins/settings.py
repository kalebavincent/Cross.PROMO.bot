from pyrogram import filters,Client, enums
from pyrogram.types import Message
import traceback,time
from database.models.user_db import get_admin,total_admin,total_users
from database.models.channel_db import total_banned_channel,total_channel
from database.models.settings_db import add_grid_size, add_list_size,add_subs_limit,get_settings
from utils.markup import admin_markup,back_markup,settings_markup,empty_markup
import logging
LOGGER = logging.getLogger(__name__)
from config import Config
LOG_CHANNEL = Config.LOG_CHANNEL
SUDO_USERS = Config.SUDO_USERS


@Client.on_callback_query(filters.regex('^stats$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def bot_stats(bot : Client , message : Message):
    users = await total_users()
    admins = await total_admin()
    channels = await total_channel()
    banned_channels = await total_banned_channel()
    
    stats=f"""<b>Total des utilisateurs :</b> {users}
<b>Total des administrateurs :</b> {admins}
<b>Nombre de canaux enregistrés :</b> {channels}
<b>Nombre de canaux bannis :</b> {banned_channels}"""
    # LOGGER.info(f"BOT STATISTICS : \n {stats}")
    await bot.send_message(message.message.chat.id,stats)
    
    
@Client.on_callback_query(filters.regex('^settings$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def settings_handler(bot: Client, message: Message):
    info = get_settings()
    
    text = f"""
🔄 Limite de abonnés : {info.get('subs_limit', 0)}
🏷 Taille de la liste : {info.get('list_size', 0)}
🏷 Taille de la grille : {info.get('grid_size', 0)}
    """
    await bot.send_message(message.from_user.id, text, reply_markup=settings_markup())

    
@Client.on_callback_query(filters.regex('^subs_limit$') &(filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def subs_limit_handler(bot : Client , message : Message):
    try:
        data=await bot.ask(message.from_user.id,"Envoyez la limite d'abonnés",reply_markup=back_markup())
        add_subs_limit(int(data.text))
        await bot.send_message(message.from_user.id,"Réglage réussi",reply_markup=empty_markup())
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',parse_mode=enums.ParseMode.HTML)
        await bot.send_message(message.message.chat.id,"<b>❌ Un problème est survenu </b>",reply_markup=empty_markup())
    

@Client.on_callback_query(filters.regex('^list_size$') &(filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def list_size_handler(bot : Client , message : Message):
    try:
        data=await bot.ask(message.from_user.id,"Envoyez la taille de la liste",reply_markup=back_markup())
        add_list_size(int(data.text))
        await bot.send_message(message.from_user.id,"Réglage réussi",reply_markup=empty_markup())
    
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',parse_mode=enums.ParseMode.HTML)
        await bot.send_message(message.message.chat.id,"<b>❌ Un problème est survenu</b>",reply_markup=empty_markup())
        
@Client.on_callback_query(filters.regex('^grid_size$') &(filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def grid_size_handler(bot : Client , message : Message):
    try:
        data=await bot.ask(message.from_user.id,"Envoyez la taille de la grille",reply_markup=back_markup())
        add_grid_size(int(data.text))
        await bot.send_message(message.from_user.id,"Réglage réussi",reply_markup=empty_markup())
    
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',parse_mode=enums.ParseMode.HTML)
        await bot.send_message(message.message.chat.id,"<b>❌ Un problème est survenu</b>",reply_markup=empty_markup())
    


    

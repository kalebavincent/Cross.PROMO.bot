from pyrogram import filters,Client, enums
from pyrogram.types import Message
import traceback,time
from database.models.user_db import get_admin,get_all,delete_user   
from database.models.channel_db import total_channel                                                                                        
from utils.markup import admin_markup,back_markup,empty_markup,announce_markup
from config import Config
LOG_CHANNEL = Config.LOG_CHANNEL
SUPPORT_GROUP = Config.SUPPORT_GROUP
SUPPORT_CHANNEL = Config.SUPPORT_CHANNEL
SUDO_USERS = Config.SUDO_USERS
import logging
LOGGER = logging.getLogger(__name__)

@Client.on_callback_query(filters.regex('^announce$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def announcement_handler(bot:Client,message:Message):
    await bot.send_message(message.from_user.id, "✅ Choisissez la catégorie de l'annonce" ,reply_markup=announce_markup())
    
    
@Client.on_callback_query(filters.regex('^close_reg$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def close_reg_handler(bot: Client, message: Message):
    total_channels = await total_channel()

    data = f"""
🔰 L'inscription a été fermée

- La liste sera bientôt disponible.
- Restez à l'écoute !

<b>Total des canaux enregistrés :</b> {total_channels}
"""

    await bot.send_message(SUPPORT_GROUP, data)
    LOGGER.info(f"Close Registration Message sent to @{SUPPORT_GROUP}")


    
@Client.on_callback_query(filters.regex('^open_reg$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def open_reg_handler(bot:Client,message:Message):
    me=await bot.get_me()
    data = f"""
🔰 𝗜𝗡𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 𝗢𝗨𝗩𝗘𝗥𝗧𝗘 🔰

➖ 𝗖𝗢𝗠𝗠𝗘𝗡𝗧 𝗣𝗔𝗥𝗧𝗜𝗖𝗜𝗣𝗘𝗥 :
1. <a href='https://t.me/{me.username}'>【 𝗖𝗹𝗶𝗾𝘂𝗲𝘇 𝗶𝗰𝗶 𝗽𝗼𝘂𝗿 𝗽𝗮𝗿𝘁𝗶𝗰𝗶𝗽𝗲𝗿 】</a>
2. 𝗔𝗽𝗽𝘂𝘆𝗲𝘇 𝘀𝘂𝗿 「 𝗗𝗲́𝗺𝗮𝗿𝗿𝗲𝗿 」
3. 𝗦𝗲́𝗹𝗲𝗰𝘁𝗶𝗼𝗻𝗻𝗲𝘇 「 𝗠𝗲𝘀 𝗰𝗮𝗻𝗮𝘂𝘅 」 𝗽𝗼𝘂𝗿 𝗰𝗼𝗻𝘀𝘂𝗹𝘁𝗲𝗿 𝘃𝗼𝘀 𝗰𝗮𝗻𝗮𝘂𝘅 𝗲𝗻𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗲́𝘀
4. 𝗡𝗼𝘂𝘃𝗲𝗮𝘂𝘅 𝗺𝗲𝗺𝗯𝗿𝗲𝘀 : 𝗜𝗻𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 𝘂𝗻𝗶𝗾𝘂𝗲, 𝗽𝗮𝘀 𝗯𝗲𝘀𝗼𝗶𝗻 𝗱𝗲 𝗿𝗲́𝗶𝗻𝘀𝗰𝗿𝗶𝗿𝗲 𝘃𝗼𝘁𝗿𝗲 𝗰𝗮𝗻𝗮𝗹 𝗽𝗼𝘂𝗿 𝗹𝗲𝘀 𝗽𝗿𝗼𝗺𝗼𝘀 𝘀𝘂𝗶𝘃𝗮𝗻𝘁𝗲𝘀.
5. 𝗔𝗻𝗰𝗶𝗲𝗻𝘀 𝗺𝗲𝗺𝗯𝗿𝗲𝘀 : 𝗟𝗲 𝗯𝗼𝘁 𝗺𝗲𝘁𝘁𝗿𝗮 𝗮̀ 𝗷𝗼𝘂𝗿 𝗮𝘂𝘁𝗼𝗺𝗮𝘁𝗶𝗾𝘂𝗲𝗺𝗲𝗻𝘁 𝗹𝗲 𝗻𝗼𝗺𝗯𝗿𝗲 𝗱'𝗮𝗯𝗼𝗻𝗻𝗲́𝘀. 𝗣𝗮𝘀 𝗱'𝗶𝗻𝗾𝘂𝗶𝗲́𝘁𝘂𝗱𝗲.

✅ 𝗥𝗘̀𝗚𝗟𝗘𝗦 𝗗𝗘 𝗣𝗔𝗥𝗧𝗜𝗖𝗜𝗣𝗔𝗧𝗜𝗢𝗡 :
- 𝟮 𝗵𝗲𝘂𝗿𝗲𝘀 𝗲𝗻 𝗵𝗮𝘂𝘁 𝗱𝗲 𝗹𝗶𝘀𝘁𝗲
- 𝟮 𝗷𝗼𝘂𝗿𝘀 𝗱𝗮𝗻𝘀 𝗹𝗲 𝗰𝗮𝗻𝗮𝗹
- 𝟮𝟰 𝗵𝗲𝘂𝗿𝗲𝘀 𝗽𝗼𝘂𝗿 𝗽𝗮𝗿𝘁𝗮𝗴𝗲𝗿 𝗹𝗮 𝗽𝗿𝗼𝗺𝗼

━━━━━━━━━━━━━━━  
⚠️ 𝗧𝗬𝗣𝗘 𝗗𝗘 𝗣𝗥𝗢𝗠𝗢𝗧𝗜𝗢𝗡 𝗔𝗖𝗖𝗘𝗣𝗧𝗘́𝗘 :
"""


    
    await bot.send_message(SUPPORT_GROUP,data)
    user_message = f""" 
ℹ️ Notification admin

✅ L'inscription a commencé

<b>Règles de la liste</b>
1. 2 heures 🔝 dans le canal
2. 2 jours dans le canal
3. 24 heures pour partager

<a href='https://t.me/{me.username}'>Cliquez ici pour participer</a>"""

    users= await get_all()
    for user in users:
        try:
            await bot.send_message(user,user_message)
            LOGGER.info(f"Open Registration Message sent to {user}")
        except Exception as e:
            LOGGER.info(f"Open Registration message not sent to {user} ({e})")
            await delete_user(user)
    await bot.send_message(message.message.chat.id, '☑️ Terminé !')
    # LOGGER.info(f"Open Registration Message send to all")
    
@Client.on_callback_query(filters.regex('^list_out$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def list_out_handler(bot:Client,message:Message):
    user_message = f"""
ℹ️ Notification admin

✅ La liste est sortie @{SUPPORT_CHANNEL}

Règles de la liste
1. 2 heures 🔝 dans le canal
2. 2 jours dans le canal
3. 24 heures pour partager"""

    users= await get_all()
    for user in users:
        try:
            await bot.send_message(user,user_message)
            # LOGGER.info(f"List out Message sent to {user}")
        except Exception as e:
            # LOGGER.info(f"List out message not sent to {user} ({e})")
            await delete_user(user)
    await bot.send_message(message.message.chat.id, '☑️ Terminé !')
    # LOGGER.info(f"Message send to all")
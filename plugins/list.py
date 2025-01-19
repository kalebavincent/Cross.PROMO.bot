from pyrogram import filters, Client, enums
from pyrogram.types import Message
import traceback, time
from database.models.user_db import get_admin
from utils.markup import admin_markup, list_markup
from config import Config
LOG_CHANNEL = Config.LOG_CHANNEL
SUDO_USERS = Config.SUDO_USERS
import logging
LOGGER = logging.getLogger(__name__)
from database.models.user_db import get_all_user_data, total_users
from database.models.channel_db import (
    total_banned_channel,
    total_channel,
    get_channel,
    get_banned_channel_list,
    get_user_channel_count
)


@Client.on_callback_query(filters.regex('^list$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def list_handler(bot: Client, message: Message):
    await bot.send_message(message.message.chat.id, "☑️ Choisissez la liste requise", reply_markup=list_markup())


@Client.on_callback_query(filters.regex('^ban_list$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def ban_list_handler(bot: Client, message: Message):
    # Utilisez await pour attendre la coroutine
    channel_count = await total_banned_channel()
    ban_channels = await get_banned_channel_list()

    # Construire le texte des canaux bannis
    text = ""
    for channel in ban_channels:
        text += str(channel) + '\n'
    
    data = f'Total des canaux bannis : {channel_count}\n\n{text}'
    await bot.send_message(message.message.chat.id, data)


@Client.on_callback_query(filters.regex('^user_list$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def user_list_handler(bot: Client, message: Message):
    # Utilisez await pour attendre la coroutine
    users = await get_all_user_data()  # Assurez-vous que cette fonction est async et attendue

    with open("users.txt", "w", encoding='UTF-8') as f:
        if isinstance(users, list):  # Si users est une liste
            for user in users:
                # Utilisez await pour obtenir le nombre de canaux enregistrés
                channel = await get_user_channel_count(user.get('chat_id'))  # Utilisation de .get() pour éviter les erreurs
                data = f"""
🆔 ID : {user.get('chat_id')}
📛 Nom : {user.get('first_name')}
👤 Nom d'utilisateur : {user.get('username')}
🗓 Inscrit depuis : {user.get('date')}
📢 Nombre de canaux enregistrés : {channel}
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
                """
                f.write(data)
        elif isinstance(users, dict):  # Si users est un dictionnaire
            for user_id, user in users.items():
                # Assurez-vous que vous accédez aux bonnes clés dans le dictionnaire
                channel = await get_user_channel_count(user.get('chat_id'))
                data = f"""
🆔 ID : {user.get('chat_id')}
📛 Nom : {user.get('first_name')}
👤 Nom d'utilisateur : {user.get('username')}
🗓 Inscrit depuis : {user.get('date')}
📢 Nombre de canaux enregistrés : {channel}
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
                """
                f.write(data)
    total_user = await total_users()
    await bot.send_document(message.from_user.id, 'users.txt', caption=f'Total des utilisateurs : {total_user}', file_name='user_list.txt')

@Client.on_callback_query(filters.regex('^channel_list$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def channel_list_handler(bot: Client, message: Message):
    # Utilisez await pour attendre la coroutine
    channels = await get_channel()

    with open("channels.txt", "w", encoding='UTF-8') as f:
        for channel in channels:
            # Vérifiez si channel est un dictionnaire ou un objet
            if isinstance(channel, dict):
                # Si c'est un dictionnaire, accédez aux valeurs par clé
                data = f"""
🆔 ID : {channel.get('channel_id', 'N/A')}
📛 Nom : {channel.get('channel_name', 'N/A')}
👤 Abonnés : {channel.get('subscribers', 'N/A')}
📄 Description : {channel.get('description', 'N/A')}
👨‍ Admin : {channel.get('admin_username', 'N/A')} [{channel.get('chat_id', 'N/A')}]
🔗 Lien d'invitation : {channel.get('invite_link', 'N/A')}
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
"""
            else:
                # Si c'est un objet, accédez directement aux attributs
                data = f"""
🆔 ID : {channel.channel_id}
📛 Nom : {channel.channel_name}
👤 Abonnés : {channel.subscribers}
📄 Description : {channel.description}
👨‍ Admin : {channel.admin_username} [{channel.chat_id}]
🔗 Lien d'invitation : {channel.invite_link}
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
"""
            f.write(data)
    total_channels = await total_channel()  
    await bot.send_document(message.from_user.id, 'channels.txt', caption=f'Total des canaux : {total_channels}', file_name='channel_list.txt')

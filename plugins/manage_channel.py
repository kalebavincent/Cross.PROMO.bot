from pyrogram import filters, Client, enums
from pyrogram.types import Message
import traceback, time
from database.models.user_db import get_admin
from database.models.channel_db import (delete_channel,
                                            ban_channel,
                                            unban_channel,
                                            is_channel_exist, 
                                            get_channel,
                                            is_channel_banned,
                                            update_subs,
                                            get_channel_by_id)
                            
from utils.markup import admin_markup, back_markup, empty_markup
from config import Config
LOG_CHANNEL = Config.LOG_CHANNEL
SUDO_USERS = Config.SUDO_USERS
import logging
LOGGER = logging.getLogger(__name__)
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, ChannelPrivate

@Client.on_callback_query(filters.regex('^ban$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def ban_channel_handler(bot: Client, message: Message):
    channel_ban = await bot.ask(message.message.chat.id, 'Transférez le message depuis le canal', reply_markup=back_markup())
    
    try:
        if channel_ban.text == '🚫 Annuler':
            await bot.send_message(message.message.chat.id, "Action annulée", reply_markup=empty_markup())
        else:
            # Vérification de l'existence du canal de manière asynchrone
            if not await is_channel_exist(channel_ban.forward_from_chat.id):
                await bot.send_message(message.message.chat.id, "Le canal n'existe pas", reply_markup=empty_markup())
            else:
                # Récupération du canal par ID, de manière asynchrone
                channel = await get_channel_by_id(int(channel_ban.forward_from_chat.id))

                # Si le canal existe, on le bannit
                await bot.send_message(channel['chat_id'], f"Votre canal {channel['channel_name']} est banni")
                await ban_channel(int(channel_ban.forward_from_chat.id))  # Assurez-vous que `ban_channel` est une coroutine si nécessaire
                await delete_channel(int(channel_ban.forward_from_chat.id))  # Assurez-vous que `delete_channel` est aussi une coroutine

                await bot.send_message(message.message.chat.id, "Canal banni", reply_markup=empty_markup())

    except Exception as e:
        # Gestion des erreurs
        LOGGER.error(e)
        await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nHeure : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
        await bot.send_message(message.from_user.id, "Quelque chose s'est mal passé", reply_markup=empty_markup())


# Commande pour débannir un canal
@Client.on_callback_query(filters.regex('^unban$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def unban_channel_handler(bot: Client, message: Message):
    channel_ban = await bot.ask(message.message.chat.id, 'Transférez le message depuis le canal', reply_markup=back_markup())
    
    try:
        # Si l'utilisateur annule l'action
        if channel_ban.text == '🚫 Annuler':
            await bot.send_message(message.message.chat.id, "Action annulée", reply_markup=empty_markup())
        else:
            # Vérification si le canal est déjà banni (coroutine)
            if not await is_channel_banned(channel_ban.forward_from_chat.id):
                await bot.send_message(message.message.chat.id, "Le canal n'est pas dans la liste noire", reply_markup=empty_markup())
            else:
                # Unban du canal (coroutine)
                await unban_channel(int(channel_ban.forward_from_chat.id))
                await bot.send_message(message.message.chat.id, "Canal débanni", reply_markup=empty_markup())
                
    except Exception as e:
        # Gestion des erreurs
        LOGGER.error(e)
        await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nHeure : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
        await bot.send_message(message.from_user.id, "Quelque chose s'est mal passé", reply_markup=empty_markup())


# Commande pour mettre à jour les abonnés des canaux
@Client.on_callback_query(filters.regex('^update_subs$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def update_subs_handler(bot: Client, message: Message):
    error_list = ""
    LOGGER.info("Mise à jour des abonnés commencée")
    
    channels = await get_channel()

    for channel in channels:
        try:
            LOGGER.info(f"Mise à jour des abonnés pour {channel['channel_name']}")
            subs = await bot.get_chat_members_count(channel['channel_id'])
            await update_subs(channel['channel_id'], subs)  
        except (ChannelPrivate, ChatAdminRequired) as e:
            LOGGER.error(f"Erreur pour le canal {channel['channel_name']}: {str(e)}")
            await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nHeure : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
            error_list += f"🆔 ID du canal : {channel['channel_name']}\n ❓ Erreur : {str(e)}\n\n"

    if error_list:
        await bot.send_message(message.message.chat.id, f"<b>Liste des erreurs</b>\n\n{error_list}")

    await bot.send_message(message.message.chat.id, "✅ Abonnés mis à jour avec succès")
    LOGGER.info("Mise à jour des abonnés terminée")


@Client.on_callback_query(filters.regex('^show_channel$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def show_channel_handler(bot: Client, message: Message):
    channel_info = await bot.ask(message.message.chat.id, 'Transférez le message depuis le canal', reply_markup=back_markup())
    
    try:
        if channel_info.text == '🚫 Annuler':
            await bot.send_message(message.message.chat.id, "Action annulée", reply_markup=empty_markup())
        else:
            channel = await get_channel_by_id(int(channel_info.forward_from_chat.id))
            
            if not channel:
                await bot.send_message(
                    message.from_user.id,
                    "Je n'ai pas trouvé vos données dans ma base de données. Si votre canal a récemment été banni puis débanni, veuillez le réinscrire pour le remettre à jour.",
                    reply_markup=empty_markup()
                )
                return 

            data = f"""
🆔 ID : {channel['channel_id']}
📛 Nom : {channel['channel_name']}
📄 Description : {channel['description']}
➖ Abonnés : {channel['subscribers']}
👨🏼‍💼 Admin : {channel['admin_username']}
🔗 Lien : {channel['invite_link']}
            """
            await bot.send_message(message.from_user.id, data)
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nHeure : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
        await bot.send_message(message.from_user.id, "Quelque chose s'est mal passé", reply_markup=empty_markup())


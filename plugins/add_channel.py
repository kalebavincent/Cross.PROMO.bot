from pyrogram import filters, Client, enums
from pyrogram.types import Message
import traceback, time
from config import Config
LOG_CHANNEL = Config.LOG_CHANNEL
SUDO_USERS = Config.SUDO_USERS
SUPPORT_GROUP = Config.SUPPORT_GROUP
import logging
LOGGER = logging.getLogger(__name__)
from database.models.channel_db import is_channel_ban, is_channel_exist, channel_data
from utils.markup import start_markup, back_markup, empty_markup
from utils.is_admin import is_bot_admin
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, ChannelPrivate
from database.models.settings_db import get_subcribers_limit


@Client.on_callback_query(filters.regex('^add_channel$'))
async def add_channel(bot: Client, message: Message):
    try:
        timeout_duration = 60

        try:
            channel = await bot.ask(
                message.message.chat.id,
                "✅ <b>Faites de ce bot un administrateur dans votre canal et envoyez :</b>\n"
                "1. Un message transféré depuis le canal.\n"
                "2. Un lien direct (ex : https://t.me/nom_du_canal).\n"
                "3. Un pseudonyme du canal (ex : @nom_du_canal).\n\n"
                "⏳ Vous avez 60 secondes pour répondre.",
                reply_markup=back_markup(),
                timeout=timeout_duration
            )
        except TimeoutError:
            await bot.send_message(
                message.message.chat.id,
                "⏳ <b>Temps écoulé ! Veuillez recommencer la procédure.</b>",
                reply_markup=empty_markup()
            )
            return

        if channel.text == '🚫 Cancel':
            await bot.send_message(
                message.message.chat.id,
                "🚫 <b>Annulé</b>",
                reply_markup=empty_markup()
            )
            return

        chat_id = message.from_user.id

        if channel.forward_from_chat:
            channel_id = channel.forward_from_chat.id
            channel_name = channel.forward_from_chat.title
        elif "t.me/" in channel.text:
            try:
                link = channel.text.strip()
                channel_info = await bot.get_chat(link)
                channel_id = channel_info.id
                channel_name = channel_info.title
            except Exception:
                await bot.send_message(chat_id, "<b>❌ Lien invalide ou le bot ne peut accéder au canal.</b>", reply_markup=empty_markup())
                return
        elif channel.text.startswith('@'):
            try:
                username = channel.text.strip()
                channel_info = await bot.get_chat(username)
                channel_id = channel_info.id
                channel_name = channel_info.title
            except Exception:
                await bot.send_message(chat_id, "<b>❌ Pseudonyme invalide ou inaccessible.</b>", reply_markup=empty_markup())
                return
        else:
            await bot.send_message(chat_id, "<b>❌ Message transféré, lien ou pseudonyme valide requis.</b>", reply_markup=empty_markup())
            return

        if await is_channel_ban(channel_id):
            await bot.send_message(chat_id, "Aww :( , Ce canal est banni.")
            return

        if await is_channel_exist(channel_id):
            await bot.send_message(chat_id, "Aww :( , Le canal existe déjà.")
            return

        if not await is_bot_admin(bot, channel_id):
            await bot.send_message(chat_id, "<b>❌ Le bot n'est pas administrateur</b>", reply_markup=empty_markup())
            return

        limit = get_subcribers_limit()
        subscribers = await bot.get_chat_members_count(channel_id)

        if subscribers < limit:
            await bot.send_message(chat_id, f"Vous avez besoin d'au moins {limit} abonnés pour vous inscrire.", reply_markup=empty_markup())
            return

        try:
            description = await bot.ask(
                chat_id,
                "<b>✅ Envoyez la description (maximum 5 mots et 2 emojis)</b>\n\n⏳ Vous avez 60 secondes pour répondre.",
                timeout=timeout_duration
            )
        except TimeoutError:
            await bot.send_message(
                chat_id,
                "⏳ <b>Temps écoulé pour envoyer la description. Veuillez recommencer la procédure.</b>",
                reply_markup=empty_markup()
            )
            return

        admin_username = message.from_user.username
        invite_link = await bot.export_chat_invite_link(channel_id)

        await channel_data(
            chat_id=chat_id,
            channel_id=channel_id,
            channel_name=channel_name,
            subscribers=subscribers,
            admin_username=admin_username,
            description=description.text,
            invite_link=invite_link
        )

        details = (
            f'✅ <b>Canal soumis avec succès</b>\n\n'
            f'ID du canal : {channel_id}\n'
            f'Nom du canal : {channel_name}\n'
            f'Abonnés : {subscribers}\n'
            f'Description : {description.text}'
        )
        await bot.send_message(chat_id, details, reply_markup=empty_markup())

        send_group_message = (
            f'✅ <b>Un nouveau canal soumis !</b>\n\n'
            f'ID du canal : {channel_id}\n'
            f'Nom du canal : {channel_name}\n'
            f'Abonnés : {subscribers}\n'
            f'Description : {description.text}\n'
            f'Soumis par : @{admin_username}'
        )
        await bot.send_message(SUPPORT_GROUP, send_group_message)
        LOGGER.info(f"Canal ajouté {channel_name}")

    except (ChannelPrivate, ChatAdminRequired) as e:
        LOGGER.error(e)
        await bot.send_message(
            LOG_CHANNEL,
            f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC',
            parse_mode=enums.ParseMode.HTML
        )
        await bot.send_message(chat_id, "<b>❌ Le bot n'est pas administrateur ou le canal est privé</b>", reply_markup=empty_markup())

    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(
            LOG_CHANNEL,
            f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC',
            parse_mode=enums.ParseMode.HTML
        )
        await bot.send_message(chat_id, "<b>❌ Action invalide</b>", reply_markup=empty_markup())

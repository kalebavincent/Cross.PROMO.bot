from pyrogram import filters, Client, enums
from pyrogram.types import Message
import traceback, time
from database.models.user_db import get_admin
from utils.markup import admin_markup, back_markup, empty_markup, promo_button_markup
from config import Config
LOG_CHANNEL = Config.LOG_CHANNEL
SUDO_USERS = Config.SUDO_USERS
SUPPORT_CHANNEL = Config.SUPPORT_CHANNEL
import logging
LOGGER = logging.getLogger(__name__)
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, ChannelPrivate
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden, ChatForbidden
from database.models.promo_db import add_paidpromo, delete_paid_promo, get_paidpromo
from database.models.channel_db import get_channel, get_channel_by_id

@Client.on_callback_query(filters.regex('^send_paid_promo$')  & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def paid_promo_handler(bot: Client, message: Message):
    error_list = ""
    try:
        # Demande de texte ou média
        msg = await bot.ask(
            message.message.chat.id,
            "**✅ Envoyer le texte avec le mode de parsing (si nécessaire)**",
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=back_markup(),
        )
        if msg.text == '🚫 Annuler':
            await bot.send_message(message.message.chat.id, "Terminé", reply_markup=empty_markup())
            return
        
        # Vérification du type de contenu
        if msg.media:
            m = await bot.send_photo(
                SUPPORT_CHANNEL,
                msg.photo.file_id,
                caption=msg.caption or "",
                parse_mode=enums.ParseMode.HTML,
                reply_markup=promo_button_markup(),
            )
        else:
            m = await bot.send_message(
                SUPPORT_CHANNEL,
                msg.text,
                reply_markup=promo_button_markup(),
                parse_mode=enums.ParseMode.HTML,
            )
        
        # Récupération des canaux et envoi des messages
        chname = await get_channel()  # Utilisation de `await`
        for x in chname:
            try:
                id_channel = await bot.forward_messages(
                    chat_id=x['channel_id'],
                    from_chat_id=SUPPORT_CHANNEL,
                    message_ids=m.id,
                )
                add_paidpromo(x['channel_id'], id_channel.id)
            except (ChatAdminRequired, ChannelPrivate, ChatWriteForbidden, ChatForbidden):
                await bot.send_message(
                    x['channel_id'],
                    f"Échec de l'envoi du message pour {x['channel_name']}\nVeuillez republier la promotion pour éviter un bannissement",
                )
                error_list += (
                    f"🆔 ID : {x['channel_id']}\n"
                    f"📛 Nom : {x['channel_name']}\n"
                    f"👨‍ Admin : @{x['admin_username']} \n"
                    f"🔗Lien : {x['invite_link']}\n"
                    "➖" * 12 + "\n"
                )
            except Exception as e:
                await bot.send_message(
                    LOG_CHANNEL,
                    f'\n<code>{traceback.format_exc()}</code>\n\nHeure : {time.ctime()} UTC',
                    parse_mode=enums.ParseMode.HTML,
                )
                print(f"Erreur : {e}")
        
        # Résumé à l'utilisateur
        await bot.send_message(message.message.chat.id, "✅ TERMINÉ", reply_markup=empty_markup())
        if error_list:
            await bot.send_message(message.from_user.id, f"Échec de l'envoi du message\n\n{error_list}")
    except Exception as e:
        print(f"Erreur inattendue : {traceback.format_exc()}")
        await bot.send_message(
            LOG_CHANNEL,
            f"Erreur inattendue\n\n<code>{traceback.format_exc()}</code>",
            parse_mode=enums.ParseMode.HTML,
        )
        
@Client.on_callback_query(filters.regex('^delete_paid_promo$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def delete_paid_promo_handler(bot: Client, message: Message):
    error_list = ""
    try:
        # Récupération des promotions payées
        promo = get_paidpromo()
        for i in promo:
            try:
                # Suppression du message
                success = await bot.delete_messages(chat_id=i["channel"], message_ids=i["message_id"])
                if not success:
                    # Si la suppression échoue, ajouter le canal à la liste d'erreurs
                    x = get_channel_by_id(i["channel"])
                    error_list += (
                        f"🆔 ID : {x['channel_id']}\n"
                        f"📛 Nom : {x['channel_name']}\n"
                        f"👨‍ Admin : @{x['admin_username']}\n"
                        f"🔗 Lien : {x['invite_link']}\n"
                        "➖" * 12 + "\n"
                    )
            except Exception as e:
                await bot.send_message(
                    LOG_CHANNEL,
                    f"Erreur lors de la suppression d'un message\n\n<code>{traceback.format_exc()}</code>",
                    parse_mode=enums.ParseMode.HTML,
                )
                print(f"Erreur : {e}")

        # Suppression des promotions de la base de données
        delete_paid_promo()

        # Confirmation de la suppression
        await bot.send_message(message.message.chat.id, "✅ TERMINÉ")
        if error_list:
            await bot.send_message(
                message.from_user.id,
                f"Échec de la suppression de certains messages :\n\n{error_list}",
                disable_web_page_preview=True,
            )
    except Exception as e:
        await bot.send_message(
            LOG_CHANNEL,
            f"Erreur inattendue\n\n<code>{traceback.format_exc()}</code>",
            parse_mode=enums.ParseMode.HTML,
        )
        print(f"Erreur inattendue : {traceback.format_exc()}")
from pyrogram import filters,Client, enums
from pyrogram.types import Message
import traceback,time
from database.models.user_db import get_admin                                                                                                    
from utils.markup import admin_markup,back_markup,empty_markup,create_post_markup
from config import Config
LOG_CHANNEL = Config.LOG_CHANNEL
SUDO_USERS = Config.SUDO_USERS
import logging
LOGGER = logging.getLogger(__name__)
from database.models.post_db import (add_button,
                                        delete_button,
                                        add_emoji,
                                        add_caption,
                                        add_bottom_text,
                                        add_top_text
                                         )
import re

@Client.on_callback_query(filters.regex('^create_post$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def create_post_handler(bot:Client,message:Message):
    await bot.send_message(message.message.chat.id,"✅ Définir le champ requis",reply_markup=create_post_markup())
    
@Client.on_callback_query(filters.regex('^set_button$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def set_button_handler(bot:Client,message:Message):
    btn_name=await bot.ask(message.message.chat.id,"<b>✅ Envoyer le nom du bouton</b>",reply_markup=back_markup())
    if btn_name.text=='🚫 Cancel':
            await bot.send_message(message.message.chat.id,"Terminé",reply_markup=empty_markup())
    else:
        btn_link=await bot.ask(message.message.chat.id,"<b>✅ Envoyer le lien du bouton</b>",reply_markup=back_markup())
        if btn_link.text=='🚫 Cancel':
            await bot.send_message(message.message.chat.id,"Terminé",reply_markup=empty_markup())
        else:
                add_button(btn_name.text,btn_link.text)
                await bot.send_message(message.message.chat.id,("<b>✅ Bouton ajouté avec succès</b>\n\n"
                                                                f"Nom : {btn_name.text}\n"
                                                                f"URL : {btn_link.text}")
                                       ,reply_markup=empty_markup())
                
@Client.on_callback_query(filters.regex('^delete_button$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def delete_button_handler(bot:Client,message:Message):
    delete_button()
    await bot.send_message(message.from_user.id,"Buttons supprimés avec succès")
    
    
@Client.on_callback_query(filters.regex('^set_emoji$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def set_emoji_handler(bot:Client,message:Message):
    msg=await bot.ask(message.message.chat.id,"**✅ Envoyer l'émoji**",parse_mode=enums.ParseMode.MARKDOWN,reply_markup=back_markup())
    if msg.text=='🚫 Cancel':
        await bot.send_message(message.message.chat.id,"Terminé",reply_markup=empty_markup())
    else:
        add_emoji(msg.text)
        await bot.send_message(message.message.chat.id,f"Emoji definis avec succès défini {msg.text}",reply_markup=empty_markup())
        
@Client.on_callback_query(filters.regex('^set_caption$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def set_caption_handler(bot:Client,message:Message):
    msg=await bot.ask(message.message.chat.id,"**✅ Envoyer le texte avec le mode de formatage (si nécessaire)**",
                        parse_mode=enums.ParseMode.MARKDOWN,
                        reply_markup=back_markup())
    if msg.text=='🚫 Cancel':
        await bot.send_message(message.message.chat.id,"Terminé",reply_markup=empty_markup())
    else:
        add_caption(msg.text)
        await bot.send_message(message.message.chat.id,f"Texte défini avec succès\n\n {msg.text}",
                                reply_markup=empty_markup(),
                                disable_web_page_preview=True) 
           
@Client.on_callback_query(filters.regex('^set_top_text$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def set_top_text_handler(bot:Client,message:Message):
    msg=await bot.ask(message.message.chat.id,"**✅ Envoyer le texte avec le mode de formatage (si nécessaire)**",
                        parse_mode=enums.ParseMode.MARKDOWN,
                        reply_markup=back_markup())
    if msg.text=='🚫 Cancel':
        await bot.send_message(message.message.chat.id,"Terminé",reply_markup=empty_markup())
    else:
        add_top_text(msg.text)
        await bot.send_message(message.message.chat.id,f"Texte défini avec succès\n\n {msg.text}",
                                reply_markup=empty_markup(),
                                disable_web_page_preview=True)    

@Client.on_callback_query(filters.regex('^set_bottom_text$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def set_bottom_text_handler(bot:Client,message:Message):
    msg=await bot.ask(message.message.chat.id,"**✅ Envoyer le texte avec le mode de formatage (si nécessaire)**",
                        parse_mode=enums.ParseMode.MARKDOWN,
                        reply_markup=back_markup())
    
    if msg.text=='🚫 Cancel':
        await bot.send_message(message.message.chat.id,"Terminé",reply_markup=empty_markup())
    else:
        add_bottom_text(msg.text)
        await bot.send_message(message.message.chat.id,f"Texte défini avec succès\n\n {msg.text}",
                                reply_markup=empty_markup(),
                                disable_web_page_preview=True)  

@Client.on_callback_query(filters.regex('^add_image$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def add_image_handler(bot: Client, message: Message):
    try:
        msg = await bot.ask(
            message.message.chat.id,
            "**✅ Envoyez une image. Appuyez sur 🚫 Cancel pour annuler.**",
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=back_markup()
        )

        if msg.text == '🚫 Cancel':
            await bot.send_message(
                message.message.chat.id,
                "Terminé.",
                reply_markup=empty_markup()
            )
            return

        if msg.photo or msg.document:
            if msg.document and not msg.document.mime_type.startswith("image/"):
                await bot.send_message(
                    message.message.chat.id,
                    "❌ Le fichier envoyé n'est pas une image. Veuillez réessayer.",
                    reply_markup=empty_markup()
                )
                return

            file_path = await bot.download_media(
                message=msg,
                file_name="image.jpg",
                progress=progress
            )

            await bot.send_message(
                message.message.chat.id,
                f"✅ Image enregistrée avec succès : `{file_path}`",
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=empty_markup(),
                disable_web_page_preview=True
            )
        else:
            await bot.send_message(
                message.message.chat.id,
                "❌ Action invalide : vous devez envoyer une image.",
                reply_markup=empty_markup()
            )
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(
            message.message.chat.id,
            "⚠️ Une erreur est survenue lors du traitement de l'image.",
            reply_markup=empty_markup()
        )


def progress(current, total):
    LOGGER.info(f"Téléchargement en cours : {current * 100 / total:.1f}%")

    

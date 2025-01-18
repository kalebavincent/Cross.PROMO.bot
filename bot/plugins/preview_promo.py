from pyrogram import filters, Client, enums
from bot.bot import Bot
from pyrogram.types import Message
import traceback, time
from bot.database.models.settings_db import get_grid_size
from bot.database.models.user_db import get_admin
from bot.utils.markup import admin_markup, back_markup, empty_markup, promo_button_markup, preview_list_markup
from bot import LOGGER, LOG_CHANNEL, SUDO_USERS, SUPPORT_CHANNEL
from bot.database.models.post_db import get_buttons, get_post
from bot.database.models.channel_db import get_channel, get_channel_by_id, chunck
from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

# Attente du générateur asynchrone pour obtenir la liste complète
async def get_chunk_data():
    a = []
    async for chunk in chunck():
        a.append(chunk)
    return a


# Charger les données de chunk avant de continuer
async def initialize_data():
    global a
    a = await get_chunk_data()


p = f"🗣Via @{SUPPORT_CHANNEL} \n1 hr Top 24 hrs🔛 in Channel.\n━━━━━━━━━━━━━━━\n<a href='tg://user?id={SUDO_USERS}'>🔴PAID PROMOTION HERE🔴</a>\n━━━━━━━━━━━━━━━\n\n"

# Gestion de la prévisualisation du message promo
@Bot.on_callback_query(filters.regex('^preview$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def preview_promo_handler(bot: Client, message: Message):
    await bot.send_message(message.message.chat.id, "✅ Choisir la liste de promotion", reply_markup=preview_list_markup())

# Prévisualisation de la promotion classique
@Bot.on_callback_query(filters.regex('^preview_classic_promo$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def preview_classic_promo_handler(bot: Client, message: Message):
    a = await get_chunk_data()
    b = get_post()# Récupération des chunks de manière asynchrone
    try:
        for i in a:
            val = ""
            for j in i:
                # Attendre la récupération du canal
                ch = await get_channel_by_id(j)  # Utilisation de 'await' pour attendre la coroutine
                val += f'{b["emoji"]}<a href="{ch["invite_link"]}">{str(ch["channel_name"])}</a>\n'
                print(b)
                dest = f"{b['set_top']}\n\n{val}\n{p}\n{b['set_bottom']}"

            await bot.send_message(message.message.chat.id, dest, reply_markup=promo_button_markup(), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
        await bot.send_message(message.message.chat.id, "**⚠️ Un problème est survenu**", parse_mode=enums.ParseMode.MARKDOWN)


# Prévisualisation de la promotion moderne
@Bot.on_callback_query(filters.regex('^preview_morden_promo$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def preview_morden_promo_handler(bot: Client, message: Message):
    a = await get_chunk_data()
    b = get_post() 
    try:
        for i in a:
            val = ""
            for j in i:
                ch = await get_channel_by_id(j)  
                val += f'<b>{str(ch["description"])}</b>\n{b["emoji"]}<a href="{ch["invite_link"]}">「Joιɴ Uѕ」</a>{b["emoji"]}\n\n'
                dest = f"{b.get('set_top', '')}\n{val}\n{p}{b.get('set_bottom', '')}"
            await bot.send_message(message.message.chat.id, dest, reply_markup=promo_button_markup(), parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
        await bot.send_message(message.message.chat.id, "**⚠️ Un problème est survenu**", parse_mode=enums.ParseMode.MARKDOWN)

# Prévisualisation de la promotion par description
@Bot.on_callback_query(filters.regex('^preview_desc_promo$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def preview_desc_promo_handler(bot: Client, message: Message):
    a = await get_chunk_data() 
    b = get_post()
    try:
        for i in a:
            val = ""
            for j in i:
                ch = await get_channel_by_id(j)  
                val += f'\n<a href="{ch["invite_link"]}"><b>{str(ch["description"])}</b></a>\n<b>––––––––––––––––––</b>\n\n'
                dest = f"{b.get('set_top', '')}\n{val}\n{p}{b.get('set_bottom', '')}"
            await bot.send_message(message.message.chat.id, dest, reply_markup=promo_button_markup(), parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
        await bot.send_message(message.message.chat.id, "**⚠️ Un problème est survenu**", parse_mode=enums.ParseMode.MARKDOWN)

# Prévisualisation de la promotion avec boutons
@Bot.on_callback_query(filters.regex('^preview_button_promo$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def preview_button_promo_handler(bot: Client, message: Message):
    a = await get_chunk_data()  # Récupérer les données des canaux
    b = get_post()  # Récupérer le message de promotion
    
    try:
        down_buttons = get_buttons()  # Récupérer les boutons additionnels
        bq = [InlineKeyboardButton(x['name'], url=x['url']) for x in down_buttons]
        
        for i in a:
            buttons = []  # Réinitialiser les boutons pour chaque groupe
            
            temp_buttons = []  # Regrouper les boutons par ligne
            for j in i:
                # Récupérer les informations du canal de manière asynchrone
                ch = await get_channel_by_id(j)
                temp_buttons.append(InlineKeyboardButton(ch['channel_name'], url=ch['invite_link']))
                tgrille = int(get_grid_size())
                
                # Ajouter une ligne après 2 boutons
                if len(temp_buttons) == tgrille:
                    buttons.append(temp_buttons)
                    temp_buttons = []
            
            # Ajouter les boutons restants
            if temp_buttons:
                buttons.append(temp_buttons)
            
            # Ajouter les boutons additionnels en bas
            buttons.append(bq)
            
            # Créer le clavier
            markup = InlineKeyboardMarkup(buttons)
            
            # Envoyer la photo avec les boutons générés
            await bot.send_photo(
                chat_id=message.message.chat.id,
                photo='bot/downloads/image.jpg',
                caption=b['set_caption'],
                reply_markup=markup
            )
    
    except Exception as e:
        # Gestion des erreurs
        LOGGER.error(e)
        await bot.send_message(
            LOG_CHANNEL,
            f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC',
            parse_mode=enums.ParseMode.HTML
        )
        await bot.send_message(
            chat_id=message.message.chat.id,
            text="**⚠️ Un problème est survenu**",
            parse_mode=enums.ParseMode.MARKDOWN
        )



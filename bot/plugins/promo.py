from pyrogram import filters,Client, enums
from bot.bot import Bot
from pyrogram.types import Message
import traceback,time
from bot.database.models.settings_db import get_grid_size
from bot.database.models.user_db import get_admin,get_user_username
from bot.utils.markup import back_markup,empty_markup,promo_button_markup,send_promo_markup 
from bot import LOGGER,LOG_CHANNEL,SUDO_USERS,SUPPORT_CHANNEL,SUPPORT_GROUP
from bot.database.models.post_db import get_buttons,get_post
from bot.database.models.channel_db  import get_channel,get_channel_by_id,chunck,get_user_channel_count
from bot.database.models.promo_db import save_message_ids,delete_promo,get_promo
from pyrogram.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardRemove
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired,ChannelPrivate
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden,ChatForbidden

async def get_chunk_data():
    a = []
    async for chunk in chunck():
        a.append(chunk)
    return a

# Charger les données de chunk avant de continuer
async def initialize_data():
    global a
    a = await get_chunk_data()

p = f"🗣Via @{SUPPORT_CHANNEL} \n1 heure Top 24 heures🔛 dans le canal.\n━━━━━━━━━━━━━━━\n<a href='tg://user?id={SUDO_USERS}'>🔴PROMOTION PAYANTE ICI🔴</a>\n━━━━━━━━━━━━━━━\n\n"
line='━━━━━━━━━━━━━━━'



@Bot.on_callback_query(filters.regex('^send_promo$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def send_promo_handler(bot:Client,message:Message):
    await bot.send_message(message.message.chat.id,"✅ Choisissez la liste de promotion",reply_markup=send_promo_markup())
    
@Bot.on_callback_query(filters.regex('^delete_promotion$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def delete_promo_handler(bot:Client,message:Message):
    error_list=""
    promo=get_promo() 
    for i in promo:
            print(i['message_id'])
            try:
                messages=await bot.delete_messages(i['channel'],i['message_id'])
                if messages is False:
                    x=get_channel_by_id(i['channel'])
                    error_list+=f"🆔 ID : {x.channel_id}\n📛 Nom : {x.channel_name}\n👨‍ Admin : @{x.admin_username} \n🔗Lien : {x.invite_link}\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
            except Exception as e:
                await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC',parse_mode=enums.ParseMode.HTML)
                LOGGER.error(e)
    delete_promo()
    await bot.send_message(message.message.chat.id,"✅ TERMINÉ")
    await bot.send_message(message.from_user.id,f"Échec de la suppression de la liste de promotion\n\n {error_list}",disable_web_page_preview=True)
    
@Bot.on_callback_query(filters.regex('^send_classic_promo$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def send_classic_promo_handler(bot: Client, message: Message):
    b = get_post()  # Fonction synchrone, pas besoin d'await ici
    a = await get_chunk_data()  # Assurez-vous que get_chunk_data est bien une coroutine

    try:
        channl = ''
        error_list = ''
        li = 1

        for i in a:
            val = ""
            userdata = ""

            for j in i:
                # Attendez correctement les coroutines
                ch = await get_channel_by_id(j)  # Attendre la coroutine
                user = await get_user_username(ch['chat_id'])  # Attendre la coroutine
                channel_count = await get_user_channel_count(ch['chat_id'])  # Attendre la coroutine
                val += f'{b["emoji"]}<a href="{ch["invite_link"]}">{str(ch["channel_name"])}</a>\n'
                dest = f"{b['set_top']}\n\n{val}\n{p}\n{b['set_bottom']}"
                userdata += f'<code>@{user} ({channel_count})</code>\n'

            forward = await bot.send_message(
                SUPPORT_CHANNEL,
                dest,
                reply_markup=promo_button_markup(),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
            await bot.send_message(SUPPORT_CHANNEL, f"Admin Liste {li}\n\n{userdata}")
            li += 1

            for x in i:
                # Attendez correctement la coroutine
                chname = await get_channel_by_id(x)  # Attendre la coroutine

                try:
                    # Forward le message et obtenir l'objet Message
                    id_channel = await bot.forward_messages(
                        chat_id=x,
                        from_chat_id=SUPPORT_CHANNEL,
                        message_ids=forward.id  # Utilisation de "id" au lieu de "message_id"
                    )
                    
                    # On accède au message envoyé pour obtenir l'id du message
                    id_channel_message_id = id_channel.id  # Utilisation de "id" au lieu de "message_id"
                    save_message_ids(x, id_channel_message_id)

                    # Correction de l'accès aux attributs
                    channl += f"✅ Nom du canal : {chname['channel_name']}\nhttp://t.me/c/{str(x)[3:]}/{str(id_channel_message_id)}\n{line}\n\n"

                except (ChatAdminRequired, ChannelPrivate, ChatWriteForbidden, ChatForbidden):
                    await bot.send_message(
                        x.chat_id,
                        f"Échec de l'envoi du message pour {x.channel_name}\nVeuillez republier la promotion pour éviter un bannissement"
                    )
                    error_list += f"🆔 ID : {x.channel_id}\n📛 Nom : {x.channel_name}\n👨‍ Admin : @{x.admin_username}\n🔗Lien : {x.invite_link}\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
                except Exception as e:
                    await bot.send_message(
                        LOG_CHANNEL,
                        f'<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',
                        parse_mode=enums.ParseMode.HTML
                    )
                    LOGGER.error(e)

            await bot.send_message(SUPPORT_CHANNEL, f"#shared avec succès\n\n{channl}", parse_mode=enums.ParseMode.MARKDOWN)
            await bot.send_message(SUPPORT_CHANNEL, f"#unsucessfull\n\n{error_list}")

    except Exception as e:
        LOGGER.error(f"Erreur lors de l'exécution de la promotion: {e}")
        await bot.send_message(
            LOG_CHANNEL,
            f"<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC",
            parse_mode=enums.ParseMode.HTML
        )
        await bot.send_message(message.chat.id, "Une erreur s'est produite. Veuillez réessayer plus tard.")
        
@Bot.on_callback_query(filters.regex('^send_standard_promo$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def send_morden_promo_handler(bot: Client, message: Message):
    b = get_post()
    a = await get_chunk_data()
    
    try:
        channl = ''
        error_list = ''
        li = 1
        
        for i in a:
            val = ""
            userdata = ""
            for j in i:
                ch = await get_channel_by_id(j)  # Attendez correctement la coroutine
                user = await get_user_username(ch['chat_id'])  # Attendez correctement la coroutine
                channel_count = await get_user_channel_count(ch['chat_id'])  # Attendez correctement la coroutine
                val += f'\n\n<b>{str(ch["description"])}</b>\n{b["emoji"]}<a href="{ch["invite_link"]}">「Rejoignez le canal」</a>{b["emoji"]}\n\n'
                dest = b['set_top'] + "\n" + val + "\n" + p + b['set_bottom']
                userdata += f'<code>@{user} ({channel_count})</code>\n'
            
            forward = await bot.send_message(
                SUPPORT_CHANNEL,
                dest,
                reply_markup=promo_button_markup(),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
            
            await bot.send_message(SUPPORT_CHANNEL, f"Admin Liste {li}\n\n{userdata}")
            li += 1
            
            for x in i:
                chname = await get_channel_by_id(x)  # Attendez correctement la coroutine
                try:
                    id_channel = await bot.forward_messages(
                        chat_id=x,
                        from_chat_id=SUPPORT_CHANNEL,
                        message_ids=forward.id
                    )
                    save_message_ids(x, id_channel.id)  # Utilisez .id pour obtenir l'ID du message
                    channl += f"✅ Nom du canal : {chname['channel_name']}\nhttp://t.me/c/{str(x)[3:]}/{str(id_channel.id)}\n{line}\n\n"
                    
                except (ChatAdminRequired, ChannelPrivate, ChatWriteForbidden, ChatForbidden):
                    await bot.send_message(
                        x.chat_id,
                        f"Échec de l'envoi du message pour {x.channel_name}\nVeuillez republier la promotion pour éviter un bannissement"
                    )
                    error_list += f"🆔 ID : {x.channel_id}\n📛 Nom : {x.channel_name}\n👨‍ Admin : @{x.admin_username} \n🔗Lien : {x.invite_link}\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
                except Exception as e:
                    await bot.send_message(
                        LOG_CHANNEL,
                        f'<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',
                        parse_mode=enums.ParseMode.HTML
                    )
                    LOGGER.error(e)
            
            await bot.send_message(SUPPORT_GROUP, f"#shared sucessfull\n\n{channl}", parse_mode=enums.ParseMode.MARKDOWN)
            await bot.send_message(SUPPORT_GROUP, f"#unsucessfull\n\n{error_list}")
    
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(
            LOG_CHANNEL,
            f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',
            parse_mode=enums.ParseMode.HTML
        )
        await bot.send_message(message.chat.id, "**⚠️ Un problème est survenu**", parse_mode=enums.ParseMode.MARKDOWN)
            
@Bot.on_callback_query(filters.regex('^send_desc_promo$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def send_desc_promo_handler(bot: Client, message: Message):
    b = get_post()
    a = await get_chunk_data()
    
    try:
        channl = ''
        error_list = ''
        li = 1
        
        for i in a:
            val = ""
            userdata = ""
            for j in i:
                ch = await get_channel_by_id(j)  # Attendez correctement la coroutine
                user = await get_user_username(ch['chat_id'])  # Attendez correctement la coroutine
                channel_count = await get_user_channel_count(ch['chat_id'])  # Attendez correctement la coroutine
                val += f'\n<a href="{ch["invite_link"]}"><b>{str(ch["description"])}</b></a>\n<b>––––––––––––––––––</b>\n\n'
                dest = b['set_top'] + "\n" + val + "\n" + p + b['set_bottom']
                userdata += f'<code>@{user} ({channel_count})</code>\n'
            
            forward = await bot.send_message(
                SUPPORT_CHANNEL,
                dest,
                reply_markup=promo_button_markup(),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
            
            await bot.send_message(SUPPORT_CHANNEL, f"Admin Liste {li}\n\n{userdata}")
            li += 1
            
            for x in i:
                chname = await get_channel_by_id(x)  # Attendez correctement la coroutine
                try:
                    id_channel = await bot.forward_messages(
                        chat_id=x,
                        from_chat_id=SUPPORT_CHANNEL,
                        message_ids=forward.id  # Utilisez forward.id pour l'ID du message
                    )
                    save_message_ids(x, id_channel.id)  # Utilisez .id pour obtenir l'ID du message
                    channl += f"✅ Nom du canal : {chname['channel_name']}\nhttp://t.me/c/{str(x)[3:]}/{str(id_channel.id)}\n{line}\n\n"
                    
                except (ChatAdminRequired, ChannelPrivate, ChatWriteForbidden, ChatForbidden):
                    await bot.send_message(
                        x.chat_id,
                        f"Échec de l'envoi du message pour {x['channel_name']}\nVeuillez republier la promotion pour éviter un bannissement"
                    )
                    error_list += f"🆔 ID : {x['channel_id']}\n📛 Nom : {x['channel_name']}\n👨‍ Admin : @{x['admin_username']} \n🔗Lien : {x['invite_link']}\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
                except Exception as e:
                    await bot.send_message(
                        LOG_CHANNEL,
                        f'<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',
                        parse_mode=enums.ParseMode.HTML
                    )
                    LOGGER.error(e)
            
            await bot.send_message(SUPPORT_GROUP, f"#shared sucessfull\n\n{channl}", parse_mode=enums.ParseMode.MARKDOWN)
            await bot.send_message(SUPPORT_GROUP, f"#unsucessfull\n\n{error_list}")
    
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(
            LOG_CHANNEL,
            f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',
            parse_mode=enums.ParseMode.HTML
        )
        await bot.send_message(message.chat.id, "**⚠️ Un problème est survenu**", parse_mode=enums.ParseMode.MARKDOWN)
            
            
@Bot.on_callback_query(filters.regex('^send_button_promo$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def send_button_promo_handler(bot: Client, message: Message):
    b = get_post()
    a = await get_chunk_data()
    
    try:
        channl = ''
        error_list = ''
        li = 1
        down_buttons = get_buttons()
        bq = [InlineKeyboardButton(x['name'], url=x['url']) for x in down_buttons]
        
        for i in a:
            userdata = ""
            buttons = []  # Réinitialiser les boutons à chaque itération
            
            # Construction des boutons par lots (2 par ligne ici)
            temp_buttons = []
            for j in i:
                ch = await get_channel_by_id(j)  # Attendez correctement la coroutine
                user = await get_user_username(ch['chat_id'])  # Attendez correctement la coroutine
                channel_count = await get_user_channel_count(ch['chat_id'])  # Attendez correctement la coroutine
                
                temp_buttons.append(InlineKeyboardButton(ch['channel_name'], url=ch['invite_link']))
                userdata += f'<code>@{user} ({channel_count})</code>\n'
                
                tgrille = int(get_grid_size())
                
                if len(temp_buttons) == tgrille:  # Ajoutez une ligne après 2 boutons
                    buttons.append(temp_buttons)
                    temp_buttons = []
            
            if temp_buttons:  # Ajoutez les boutons restants
                buttons.append(temp_buttons)
            
            # Ajoutez les boutons additionnels en bas
            buttons += [bq]
            
            # Créez le clavier
            markup = InlineKeyboardMarkup(buttons)
            
            # Vérification d'envoi du message avec une photo
            forward = await bot.send_photo(
                SUPPORT_CHANNEL,
                'bot/downloads/image.jpg',
                caption=b['set_caption'],
                reply_markup=markup
            )
            
            # Vérifiez que nous avons bien un message renvoyé
            if forward and hasattr(forward, 'id'):
                forward_message_id = forward.id  # Utilisez 'id' à la place de 'message_id'
            else:
                LOGGER.error("Erreur: Le message n'a pas été envoyé correctement ou ne contient pas 'id'.")
                return  # Sortir de la fonction si le message n'a pas été envoyé correctement
            
            await bot.send_message(SUPPORT_CHANNEL, f"Admin Liste {li}\n\n{userdata}")
            li += 1
            
            for x in i:
                chname = await get_channel_by_id(x)  # Attendez correctement la coroutine
                try:
                    id_channel = await bot.forward_messages(
                        chat_id=x,
                        from_chat_id=SUPPORT_CHANNEL,
                        message_ids=forward_message_id  # Utilisez forward_message_id, si c'est valide
                    )
                    save_message_ids(x, id_channel.id)  # Utilisez '.id' pour l'ID du message
                    channl += f"✅ Nom du canal : {chname['channel_name']}\nhttp://t.me/c/{str(x)[3:]}/{str(id_channel.id)}\n{line}\n\n"
                
                except (ChatAdminRequired, ChannelPrivate, ChatWriteForbidden, ChatForbidden):
                    await bot.send_message(
                        x.chat_id,
                        f"Échec de l'envoi du message pour {x['channel_name']}\nVeuillez republier la promotion pour éviter un bannissement"
                    )
                    error_list += f"🆔 ID : {x['channel_id']}\n📛 Nom : {x['channel_name']}\n👨‍ Admin : @{x['admin_username']} \n🔗Lien : {x['invite_link']}\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
                except Exception as e:
                    await bot.send_message(
                        LOG_CHANNEL,
                        f'<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',
                        parse_mode=enums.ParseMode.HTML
                    )
                    LOGGER.error(e)
            
            await bot.send_message(SUPPORT_GROUP, f"#shared successful\n\n{channl}", parse_mode=enums.ParseMode.MARKDOWN)
            await bot.send_message(SUPPORT_GROUP, f"#unsuccessful\n\n{error_list}")
    
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(
            LOG_CHANNEL,
            f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',
            parse_mode=enums.ParseMode.HTML
        )
        await bot.send_message(message.chat.id, "**⚠️ Un problème est survenu**", parse_mode=enums.ParseMode.MARKDOWN)



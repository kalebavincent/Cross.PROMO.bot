from pyrogram import filters,Client, enums
from pyrogram.types import Message
import traceback,time
from database.models.settings_db import get_grid_size
from database.models.user_db import get_admin,get_user_username
from utils.markup import back_markup,empty_markup,promo_button_markup,send_promo_markup 
from config import Config
LOG_CHANNEL = Config.LOG_CHANNEL
SUDO_USERS = Config.SUDO_USERS
SUPPORT_CHANNEL = Config.SUPPORT_CHANNEL
SUPPORT_GROUP = Config.SUPPORT_GROUP
import logging
LOGGER = logging.getLogger(__name__)
from database.models.post_db import get_buttons,get_post
from database.models.channel_db  import get_channel,get_channel_by_id,chunck,get_user_channel_count
from database.models.promo_db import save_message_ids,delete_promo,get_promo
from pyrogram.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardRemove
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired,ChannelPrivate
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden,ChatForbidden
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import (
    ChatAdminRequired, 
    ChannelPrivate, 
    ChatWriteForbidden, 
    ChatForbidden, 
    UserBannedInChannel, 
    PeerIdInvalid, 
    RPCError
)
async def get_chunk_data():
    a = []
    async for chunk in chunck():
        a.append(chunk)
    return a

async def initialize_data():
    global a
    a = await get_chunk_data()

p = f"🗣Via @{SUPPORT_CHANNEL} \n1 heure Top 24 heures🔛 dans le canal.\n━━━━━━━━━━━━━━━\n<a href='tg://user?id={SUDO_USERS}'>🔴PROMOTION PAYANTE ICI🔴</a>\n━━━━━━━━━━━━━━━\n\n"
line='━━━━━━━━━━━━━━━'



@Client.on_callback_query(filters.regex('^send_promo$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def send_promo_handler(bot:Client,message:Message):
    await bot.send_message(message.message.chat.id,"✅ Choisissez la liste de promotion",reply_markup=send_promo_markup())
    
@Client.on_callback_query(filters.regex('^delete_promotion$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
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
    
@Client.on_callback_query(filters.regex('^send_classic_promo$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def send_classic_promo_handler(bot: Client, message: Message):
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
                ch = await get_channel_by_id(j)
                user = await get_user_username(ch['chat_id'])  
                channel_count = await get_user_channel_count(ch['chat_id']) 
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
                chname = await get_channel_by_id(x)  

                try:
                    id_channel = await bot.forward_messages(
                        chat_id=x,
                        from_chat_id=SUPPORT_CHANNEL,
                        message_ids=forward.id  
                    )
                    
                  
                    id_channel_message_id = id_channel.id
                    save_message_ids(x, id_channel_message_id)

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
        
@Client.on_callback_query(filters.regex('^send_standard_promo$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
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
                ch = await get_channel_by_id(j)
                user = await get_user_username(ch['chat_id'])
                channel_count = await get_user_channel_count(ch['chat_id']) 
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
                chname = await get_channel_by_id(x)
                try:
                    id_channel = await bot.forward_messages(
                        chat_id=x,
                        from_chat_id=SUPPORT_CHANNEL,
                        message_ids=forward.id
                    )
                    save_message_ids(x, id_channel.id)  
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
            
@Client.on_callback_query(filters.regex('^send_desc_promo$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
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
                ch = await get_channel_by_id(j) 
                user = await get_user_username(ch['chat_id'])  
                channel_count = await get_user_channel_count(ch['chat_id']) 
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
                chname = await get_channel_by_id(x)  
                try:
                    id_channel = await bot.forward_messages(
                        chat_id=x,
                        from_chat_id=SUPPORT_CHANNEL,
                        message_ids=forward.id  
                    )
                    save_message_ids(x, id_channel.id)  
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
            
            
@Client.on_callback_query(filters.regex('^send_button_promo$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def send_button_promo_handler(bot: Client, message):
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
            buttons = []  

            temp_buttons = []
            for j in i:
                ch = await get_channel_by_id(j)  
                user = await get_user_username(ch['chat_id'])
                channel_count = await get_user_channel_count(ch['chat_id'])

                temp_buttons.append(InlineKeyboardButton(b['emoji'] + ch['channel_name'] + b['emoji'], url=ch['invite_link']))
                userdata += f'<code>@{user} ({channel_count})</code>\n'

                tgrille = int(get_grid_size())
                if len(temp_buttons) == tgrille:
                    buttons.append(temp_buttons)
                    temp_buttons = []

            if temp_buttons:
                buttons.append(temp_buttons)

            buttons += [bq]
            markup = InlineKeyboardMarkup(buttons)

            for x in i:
                chname = await get_channel_by_id(x)
                try:
                    chat_member = await bot.get_chat_member(x, "me")
                    if not chat_member.can_post_messages:
                        raise ChatWriteForbidden(f"Le bot n'a pas la permission de publier dans {chname['channel_name']}")

                    sent_message = await bot.send_photo(
                        chat_id=x,
                        photo='downloads/image.jpg',
                        caption=b['set_caption'],
                        reply_markup=markup
                    )
                    save_message_ids(x, sent_message.id)

                    channl += f"✅ Nom du canal : {chname['channel_name']}\nhttp://t.me/c/{str(x)[3:]}/{sent_message.id}\n{'-'*40}\n\n"
                except ChatAdminRequired:
                    error_list += f"⚠️ Le bot n'est pas admin dans {chname['channel_name']}\n"
                except ChatWriteForbidden:
                    error_list += f"⚠️ Le bot ne peut pas publier dans {chname['channel_name']}, permissions insuffisantes\n"
                except ChannelPrivate:
                    error_list += f"⚠️ Le canal {chname['channel_name']} est privé ou inaccessible\n"
                except ChatForbidden:
                    error_list += f"⚠️ Le bot est banni du canal {chname['channel_name']}\n"
                except UserBannedInChannel:
                    error_list += f"⚠️ Le bot est banni dans {chname['channel_name']}\n"
                except PeerIdInvalid:
                    error_list += f"⚠️ ID de canal invalide pour {chname['channel_name']}\n"
                except RPCError as e:
                    error_list += f"⚠️ Erreur RPC: {e}\n"
                except Exception as e:
                    LOGGER.error(f"Erreur lors de l'envoi dans {x}: {e}")
                    await bot.send_message(
                        LOG_CHANNEL,
                        f'<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',
                        parse_mode=enums.ParseMode.HTML
                    )

            await bot.send_message(SUPPORT_GROUP, f"#PartageRéussi ✅\n\n{channl}" if channl else "**Aucun succès**", parse_mode=enums.ParseMode.MARKDOWN)
            await bot.send_message(SUPPORT_GROUP, f"#Échecs ❌\n\n{error_list}" if error_list else "**Aucun échec signalé**")

            li += 1

    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(
            LOG_CHANNEL,
            f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',
            parse_mode=enums.ParseMode.HTML
        )
        await bot.send_message(message.chat.id, "**⚠️ Une erreur est survenue lors de l'exécution**", parse_mode=enums.ParseMode.MARKDOWN)
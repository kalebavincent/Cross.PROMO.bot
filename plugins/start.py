from pyrogram import filters,Client, enums
from pyrogram.types import Message
import traceback,time
from bot import LOGGER,LOG_CHANNEL,SUDO_USERS
from bot.bot import Bot
from bot.utils.markup import empty_markup, start_markup,admin_markup
from bot.database.models.user_db import add_user,get_admin

@Bot.on_message(filters.command('start') & filters.private)
async def start_handler(bot : Client, message: Message):
    await bot.send_message(message.chat.id,"Bonjour **{}**".format(message.chat.first_name),parse_mode=enums.ParseMode.MARKDOWN,reply_markup=start_markup())
    await add_user(message)
    
@Bot.on_message(filters.command('admin_start') & filters.private & filters.user(get_admin()))
async def admin_start_handler(bot : Client, message : Message):
    LOGGER.info(f"Admin logged in {message.chat.id}")
    await bot.send_message(message.chat.id,"✅ Vous êtes connecté en tant qu'administrateur",reply_markup=admin_markup())


@Bot.on_callback_query(filters.regex('^back$'))
async def back_handler(bot : Client,message : Message):
    await bot.delete_messages(message.message.chat.id,message.message.id)
    
@Bot.on_callback_query(filters.regex('^help$'))
async def help_handler(bot : Client,message : Message):
    await bot.send_message(message.message.chat.id,"✅ En Consturction...",reply_markup=empty_markup())

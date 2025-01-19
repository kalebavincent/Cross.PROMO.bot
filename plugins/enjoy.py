import asyncio
from pyrogram import Client, filters, enums
from helper.ms_gen import ReactionMessage

last_sent_messages = {}

@Client.on_message(filters.channel | filters.group)
async def on_new_post(client, message):
    chat_id = message.chat.id
    me = await client.get_me()
    bot_username = me.username
    
    permissions = 1
    if permissions == 1:
        if chat_id in last_sent_messages:
            last_message_id = last_sent_messages[chat_id]
            try:
                await client.delete_messages(chat_id, last_message_id)
            except Exception:
                pass

        ms = ReactionMessage()
        message_text = ms.get_random_message()
        try:
            new_message = await client.send_message(
                chat_id, 
                f"||**{message_text}** \n @{bot_username}||",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            last_sent_messages[chat_id] = new_message.id
        except Exception:
            pass

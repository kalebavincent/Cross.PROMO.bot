import asyncio
from pyrogram import Client, filters, enums
from helper.ms_gen import ReactionMessage

last_sent_messages = {}
comments_status = {}

@Client.on_message(filters.channel | filters.group)
async def handle_messages(client, message):
    chat_id = message.chat.id
    me = await client.get_me()
    bot_username = me.username

    if message.text and message.text.strip() == "/setoffcommentaire":
        comments_status[chat_id] = False
        confirmation_message = await message.reply_text(
            "Les commentaires ont été désactivés pour ce canal ou groupe.",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        await asyncio.sleep(10)
        await confirmation_message.delete()
        return

    if message.text and message.text.strip() == "/setoncommentaire":
        comments_status[chat_id] = True
        confirmation_message = await message.reply_text(
            "Les commentaires ont été activés pour ce canal ou groupe.",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        await asyncio.sleep(10)
        await confirmation_message.delete()
        return

    if comments_status.get(chat_id, False):
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
                return

            try:
                info_message = await client.send_message(
                    chat_id,
                    "Envoyez `/setoffcommentaire` pour désactiver les commentaires.",
                    parse_mode=enums.ParseMode.MARKDOWN
                )
                await asyncio.sleep(5)
                await info_message.delete()
            except Exception:
                pass

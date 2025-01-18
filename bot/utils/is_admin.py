
from pyrogram import Client, enums
from bot import LOGGER

async def is_bot_admin(bot: Client, chat_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, bot.me.id)
        return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
    except Exception as e:
        LOGGER.error(f"Erreur lors de la vérification de l'administration : {e}")
        return False
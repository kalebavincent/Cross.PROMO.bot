
from pyrogram import Client, enums
import logging
LOGGER = logging.getLogger(__name__)


async def is_bot_admin(bot: Client, chat_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, bot.me.id)
        return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
    except Exception as e:
        return False
from pyrogram import Client, filters
from pyrogram.types import Message

from MusikVcg.helpers.channelmusic import get_chat_id
from MusikVcg.services.callsmusic.callsmusic import remove


@Client.on_message(filters.voice_chat_ended)
async def voice_chat_ended(_, message: Message):
    try:
        remove(get_chat_id(message.chat))
    except Exception:
        pass

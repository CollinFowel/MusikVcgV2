# Daisyxmusic (Telegram bot project )
# Copyright (C) 2021  Inukaasith

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pyrogram import Client, filters
from pyrogram.types import Message

from MusikVcg.config import PMPERMIT, SUDO_USERS
from MusikVcg.services.callsmusic import client as USER

PMSET = True
pchats = []


@USER.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: USER, message: Message):
    if PMPERMIT == "ENABLE":
        if PMSET:
            chat_id = message.chat.id
            if chat_id in pchats:
                return
            await USER.send_message(
                message.chat.id,
                "Hai 👋 \n\n✨ Saya bot musik yang dibuat untuk memutar musik di obrolan suara Grup & Channel Telegram.\n\n⚡ Bot ini memiliki fitur : \n ㅤ• Memutar musik di obrolan suara.\n ㅤ• Mendownload lagu.\n ㅤ• Mendownload video.\n\n ❖ Managed by : [Owner](https://t.me/xxstanme) \n ㅤ",
            )
            return


@Client.on_message(filters.command(["/pmpermit"]))
async def bye(client: Client, message: Message):
    if message.from_user.id in SUDO_USERS:
        global PMSET
        text = message.text.split(" ", 1)
        queryy = text[1]
        if queryy == "on":
            PMSET = True
            await message.reply_text("Pmpermit Diaktifkan")
            return
        if queryy == "off":
            PMSET = None
            await message.reply_text("Pmpermit Dimatikan")
            return


@USER.on_message(filters.text & filters.private & filters.me)
async def autopmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if not chat_id in pchats:
        pchats.append(chat_id)
        await message.reply_text("Bot penjawab otomatis dinonaktifkan, karena Anda telah diizinkan untuk melakukan chat. abaikan pesan ini")
        return
    message.continue_propagation()


@USER.on_message(filters.command("a", [".", ""]) & filters.me & filters.private)
async def pmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if not chat_id in pchats:
        pchats.append(chat_id)
        await message.reply_text("Anda telah diizinkan untuk melakukan chat")
        return
    message.continue_propagation()


@USER.on_message(filters.command("da", [".", ""]) & filters.me & filters.private)
async def rmpmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if chat_id in pchats:
        pchats.remove(chat_id)
        await message.reply_text("Anda tidak diizinkan melakukan chat")
        return
    message.continue_propagation()

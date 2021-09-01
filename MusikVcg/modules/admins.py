# Calls Music 1 - Telegram bot for streaming audio in group calls
# Copyright (C) 2021  Roj Serbest

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

# Modified by @InukaAsith

# Added /auth and /deauth by azimazizov9150 <https://github.com/azimazizov9150>

from asyncio import QueueEmpty
from MusikVcg.config import que
from pyrogram import Client, filters
from pyrogram.types import Message

from MusikVcg.function.admins import admins
from MusikVcg.helpers.channelmusic import get_chat_id
from MusikVcg.helpers.decorators import authorized_users_only, errors
from MusikVcg.helpers.filters import command, other_filters
from MusikVcg.services.callsmusic import callsmusic
from MusikVcg.services.queues import queues

# By azimazizov9150 <https://github.com/azimazizov9150>

@Client.on_message(filters.command("reload"))
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text("✅ Bot telah aktif\n✅ Daftar admin diperbaharui!\n\n✨ **Join Grup kita yaa @ChatBotXanon **")


@Client.on_message(filters.command("auth"))
@authorized_users_only
async def authenticate(client, message):
    global admins
    if not message.reply_to_message:
        await message.reply("reply ke orang yg kamu mau kasih izin akses penuh bot ini")
        return
    if message.reply_to_message.from_user.id not in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.append(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply("berhasil memberikan izin akses penuh.")
    else:
        await message.reply("pengguna sudah diizinkan")


@Client.on_message(filters.command("deauth"))
@authorized_users_only
async def deautenticate(client, message):
    global admins
    if not message.reply_to_message:
        await message.reply("reply ke orang yg kamu mau hapus izin akses penuh bot ini")
        return
    if message.reply_to_message.from_user.id in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.remove(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply("berhasil menghapus izin akses penuh")
    else:
        await message.reply("pengguna sudah dihapus dari izin")

        
@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        await message.reply_text("**Tidak ada lagu yang sedang diputar !**")
    else:
        await callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("▶️ Lagu dijeda!")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        await message.reply_text("**Tidak ada lagu yang sedang dijeda !**")
    else:
        await callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("⏸ Lagu tidak lagi dijeda!")


@Client.on_message(command("end") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        await message.reply_text("**Tidak ada lagu yang sedang diputar !**")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        await callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("❌ **Memberhentikan lagu !**")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        await message.reply_text("**Tidak ada lagu yang sedang diputar untuk diskip !**")
    else:
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            await callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            await callsmusic.pytgcalls.change_stream(
                chat_id, queues.get(chat_id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"- Melewati lagu **{skip[0]}**\n- Lagu yang diputar sekarang **{qeue[0][0]}**")

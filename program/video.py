import asyncio
import re

from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2, UPDATES_CHANNEL
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.doozy import call_py, user
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:70]
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & other_filters)
async def vplay(c: Client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("⏹", callback_data="cbstop"),
                InlineKeyboardButton("⏸", callback_data="cbpause"),
                InlineKeyboardButton("▶️", callback_data="cbresume"),

            ],[
                InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("ʏᴏᴜ'ʀᴇ ᴀɴ __ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ__ !\n\n» ʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜꜱᴇʀ ᴀᴄᴄᴏᴜɴᴛ ꜰʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛꜱ.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 ᴛᴏ ᴜꜱᴇ ᴍᴇ, ɪ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ **ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀ** ᴡɪᴛʜ ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ **ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ**:\n\n» ❌ __ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ__\n» ❌ __ʀᴇꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ__\n» ❌ __ᴀᴅᴅ ᴜꜱᴇʀꜱ__\n» ❌ __ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ__\n\nᴅᴀᴛᴀ ɪꜱ **ᴜᴘᴅᴀᴛᴇᴅ** ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀꜰᴛᴇʀ ʏᴏᴜ **ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "ᴍɪꜱꜱɪɴɢ ʀᴇQᴜɪʀᴇᴅ ᴘᴇʀᴍɪꜱꜱɪᴏɴ:" + "\n\n» ❌ __ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "ᴍɪꜱꜱɪɴɢ ʀᴇQᴜɪʀᴇᴅ ᴘᴇʀᴍɪꜱꜱɪᴏɴ:" + "\n\n» ❌ __ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("ᴍɪꜱꜱɪɴɢ ʀᴇQᴜɪʀᴇᴅ ᴘᴇʀᴍɪꜱꜱɪᴏɴ:" + "\n\n» ❌ __ᴀᴅᴅ ᴜꜱᴇʀꜱ__")
        return
    if not a.can_restrict_members:
        await m.reply_text("ᴍɪꜱꜱɪɴɢ ʀᴇQᴜɪʀᴇᴅ ᴘᴇʀᴍɪꜱꜱɪᴏɴ:" + "\n\n» ❌ __ʀᴇꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ__")
        return
    try:
        ubot = await user.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **ɪꜱ ʙᴀɴɴᴇᴅ ɪɴ ɢʀᴏᴜᴘ** {m.chat.title}\n\n» **ᴜɴʙᴀɴ ᴛʜᴇ ᴜꜱᴇʀʙᴏᴛ ꜰɪʀꜱᴛ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **ᴜꜱᴇʀʙᴏᴛ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴊᴏɪɴ**\n\n**ʀᴇᴀꜱᴏɴ**: `{e}`")
                return
        else:
            try:
                pope = await c.export_chat_invite_link(chat_id)
                pepo = await c.revoke_chat_invite_link(chat_id, pope)
                await user.join_chat(pepo.invite_link)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **ᴜꜱᴇʀʙᴏᴛ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴊᴏɪɴ**\n\n**ʀᴇᴀꜱᴏɴ**: `{e}`"
                )

    if replied:
        if replied.video or replied.document:
            loser = await replied.reply("📥 **ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» __ᴏɴʟʏ 720, 480, 360 ᴀʟʟᴏᴡᴇᴅ__ \n💡 **ɴᴏᴡ ꜱᴛʀᴇᴀᴍɪɴɢ ᴠɪᴅᴇᴏ ɪɴ 720ᴘ**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                elif replied.document:
                    songname = replied.document.file_name[:70]
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ᴛʜᴇ Qᴜᴇᴜᴇ**\n\n🏷 **ɴᴀᴍᴇ:** [{songname}]({link})\n💭 **ᴄʜᴀᴛ:** `{chat_id}`\n🎧 **ʀᴇQᴜᴇꜱᴛ ʙʏ:** {requester}\n🔢 **ᴀᴛ ᴘᴏꜱɪᴛɪᴏɴ »** `{pos}`",
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"💡 **ᴠɪᴅᴇᴏ ꜱᴛʀᴇᴀᴍɪɴɢ ꜱᴛᴀʀᴛᴇᴅ.**\n\n🏷 **ɴᴀᴍᴇ:** [{songname}]({link})\n💭 **ᴄʜᴀᴛ:** `{chat_id}`\n💡 **ꜱᴛᴀᴛᴜꜱ:** `ᴘʟᴀʏɪɴɢ`\n🎧 **ʀᴇQᴜᴇꜱᴛ ʙʏ:** {requester}",
                    reply_markup=keyboard,
                )
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» ʀᴇᴘʟʏ ᴛᴏ ᴀɴ **ᴠɪᴅᴇᴏ ꜰɪʟᴇ** ᴏʀ **ɢɪᴠᴇ ꜱᴏᴍᴇᴛʜɪɴɢ ᴛᴏ ꜱᴇᴀʀᴄʜ.**"
                )
            else:
                loser = await m.reply("🔎 **ꜱᴇᴀʀᴄʜɪɴɢ...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **ɴᴏ ʀᴇꜱᴜʟᴛꜱ ꜰᴏᴜɴᴅ.**")
                else:
                    songname = search[0]
                    url = search[1]
                    doozy, ytlink = await ytdl(url)
                    if doozy == 0:
                        await loser.edit(f"❌ ʏᴛ-ᴅʟ ɪꜱꜱᴜᴇꜱ ᴅᴇᴛᴇᴄᴛᴇᴅ\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{IMG_1}",
                                caption=f"💡 **ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ᴛʜᴇ Qᴜᴇᴜᴇ**\n\n🏷 **ɴᴀᴍᴇ:** [{songname}]({url})\n💭 **ᴄʜᴀᴛ:** `{chat_id}`\n🎧 **ʀᴇQᴜᴇꜱᴛ ʙʏ:** {requester}\n🔢 **ᴀᴛ ᴘᴏꜱɪᴛɪᴏɴ »** `{pos}`",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        amaze,
                                    ),
                                    stream_type=StreamType().pulse_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=f"{IMG_2}",
                                    caption=f"💡 **ᴠɪᴅᴇᴏ ꜱᴛʀᴇᴀᴍɪɴɢ ꜱᴛᴀʀᴛᴇᴅ.**\n\n🏷 **ɴᴀᴍᴇ:** [{songname}]({url})\n💭 **ᴄʜᴀᴛ:** `{chat_id}`\n💡 **ꜱᴛᴀᴛᴜꜱ:** `ᴘʟᴀʏɪɴɢ`\n🎧 **ʀᴇQᴜᴇꜱᴛ ʙʏ:** {requester}",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await loser.delete()
                                await m.reply_text(f"🚫 ᴇʀʀᴏʀ: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» ʀᴇᴘʟʏ ᴛᴏ ᴀɴ **ᴠɪᴅᴇᴏ ꜰɪʟᴇ** ᴏʀ **ɢɪᴠᴇ ꜱᴏᴍᴇᴛʜɪɴɢ ᴛᴏ ꜱᴇᴀʀᴄʜ.**"
            )
        else:
            loser = await m.reply("🔎 **ꜱᴇᴀʀᴄʜɪɴɢ...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("❌ **ɴᴏ ʀᴇꜱᴜʟᴛꜱ ꜰᴏᴜɴᴅ.**")
            else:
                songname = search[0]
                url = search[1]
                doozy, ytlink = await ytdl(url)
                if doozy == 0:
                    await loser.edit(f"❌ ʏᴛ-ᴅʟ ɪꜱꜱᴜᴇꜱ ᴅᴇᴛᴇᴄᴛᴇᴅ\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=f"{IMG_1}",
                            caption=f"💡 **ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ᴛʜᴇ Qᴜᴇᴜᴇ**\n\n🏷 **ɴᴀᴍᴇ:** [{songname}]({url})\n💭 **ᴄʜᴀᴛ:** `{chat_id}`\n🎧 **ʀᴇQᴜᴇꜱᴛ ʙʏ:** {requester}\n🔢 **ᴀᴛ ᴘᴏꜱɪᴛɪᴏɴ »** `{pos}`",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{IMG_2}",
                                caption=f"💡 **ᴠɪᴅᴇᴏ ꜱᴛʀᴇᴀᴍɪɴɢ ꜱᴛᴀʀᴛᴇᴅ.**\n\n🏷 **ɴᴀᴍᴇ:** [{songname}]({url})\n💭 **ᴄʜᴀᴛ:** `{chat_id}`\n💡 **ꜱᴛᴀᴛᴜꜱ:** `ᴘʟᴀʏɪɴɢ`\n🎧 **ʀᴇQᴜᴇꜱᴛ ʙʏ:** {requester}",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await loser.delete()
                            await m.reply_text(f"🚫 ᴇʀʀᴏʀ: `{ep}`")


@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & other_filters)
async def vs(c: Client, m: Message):
    m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("⏹", callback_data="cbstop"),
                InlineKeyboardButton("⏸", callback_data="cbpause"),
                InlineKeyboardButton("▶️", callback_data="cbresume"),

            ],[
                InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("ʏᴏᴜ'ʀᴇ ᴀɴ __ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ__ !\n\n» ʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜꜱᴇʀ ᴀᴄᴄᴏᴜɴᴛ ꜰʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛꜱ.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 ᴛᴏ ᴜꜱᴇ ᴍᴇ, ɪ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ **ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀ** ᴡɪᴛʜ ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ **ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ**:\n\n» ❌ __ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ__\n» ❌ __ʀᴇꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ__\n» ❌ __ᴀᴅᴅ ᴜꜱᴇʀꜱ__\n» ❌ __ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ__\n\nᴅᴀᴛᴀ ɪꜱ **ᴜᴘᴅᴀᴛᴇᴅ** ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀꜰᴛᴇʀ ʏᴏᴜ **ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "ᴍɪꜱꜱɪɴɢ ʀᴇQᴜɪʀᴇᴅ ᴘᴇʀᴍɪꜱꜱɪᴏɴ:" + "\n\n» ❌ __ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "ᴍɪꜱꜱɪɴɢ ʀᴇQᴜɪʀᴇᴅ ᴘᴇʀᴍɪꜱꜱɪᴏɴ:" + "\n\n» ❌ __ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("ᴍɪꜱꜱɪɴɢ ʀᴇQᴜɪʀᴇᴅ ᴘᴇʀᴍɪꜱꜱɪᴏɴ:" + "\n\n» ❌ __ᴀᴅᴅ ᴜꜱᴇʀꜱ__")
        return
    if not a.can_restrict_members:
        await m.reply_text("ᴍɪꜱꜱɪɴɢ ʀᴇQᴜɪʀᴇᴅ ᴘᴇʀᴍɪꜱꜱɪᴏɴ:" + "\n\n» ❌ __ʀᴇꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ__")
        return
    try:
        ubot = await user.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **ɪꜱ ʙᴀɴɴᴇᴅ ɪɴ ɢʀᴏᴜᴘ** {m.chat.title}\n\n» **ᴜɴʙᴀɴ ᴛʜᴇ ᴜꜱᴇʀʙᴏᴛ ꜰɪʀꜱᴛ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **ᴜꜱᴇʀʙᴏᴛ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴊᴏɪɴ**\n\n**ʀᴇᴀꜱᴏɴ**: `{e}`")
                return
        else:
            try:
                pope = await c.export_chat_invite_link(chat_id)
                pepo = await c.revoke_chat_invite_link(chat_id, pope)
                await user.join_chat(pepo.invite_link)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **ᴜꜱᴇʀʙᴏᴛ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴊᴏɪɴ**\n\n**ʀᴇᴀꜱᴏɴ**: `{e}`"
                )

    if len(m.command) < 2:
        await m.reply("» ɢɪᴠᴇ ᴍᴇ ᴀ ʟɪᴠᴇ-ʟɪɴᴋ/ᴍ3ᴜ8 ᴜʀʟ/ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ ᴛᴏ ꜱᴛʀᴇᴀᴍ.")
    else:
        if len(m.command) == 2:
            link = m.text.split(None, 1)[1]
            Q = 720
            loser = await m.reply("🔄 **ᴘʀᴏᴄᴇꜱꜱɪɴɢ ꜱᴛʀᴇᴀᴍ...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            link = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply(
                    "» __ᴏɴʟʏ 720, 480, 360 ᴀʟʟᴏᴡᴇᴅ__ \n💡 **ɴᴏᴡ ꜱᴛʀᴇᴀᴍɪɴɢ ᴠɪᴅᴇᴏ ɪɴ 720ᴘ**"
                )
            loser = await m.reply("🔄 **ᴘʀᴏᴄᴇꜱꜱɪɴɢ ꜱᴛʀᴇᴀᴍ...**")
        else:
            await m.reply("**/vstream {link} {720/480/360}**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            doozy, livelink = await ytdl(link)
        else:
            livelink = link
            doozy = 1

        if doozy == 0:
            await loser.edit(f"❌ ʏᴛ-ᴅʟ ɪꜱꜱᴜᴇꜱ ᴅᴇᴛᴇᴄᴛᴇᴅ\n\n» `{ytlink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ᴛʜᴇ Qᴜᴇᴜᴇ**\n\n💭 **ᴄʜᴀᴛ:** `{chat_id}`\n🎧 **ʀᴇQᴜᴇꜱᴛ ʙʏ:** {requester}\n🔢 **ᴀᴛ ᴘᴏꜱɪᴛɪᴏɴ »** `{pos}`",
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                    await loser.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        caption=f"💡 **[ʟɪᴠᴇ ꜱᴛʀᴇᴀᴍ ᴠɪᴅᴇᴏ]({link}) ꜱᴛᴀʀᴛᴇᴅ.**\n\n💭 **ᴄʜᴀᴛ:** `{chat_id}`\n💡 **ꜱᴛᴀᴛᴜꜱ:** `ᴘʟᴀʏɪɴɢ`\n🎧 **ʀᴇQᴜᴇꜱᴛ ʙʏ:** {requester}",
                        reply_markup=keyboard,
                    )
                except Exception as ep:
                    await loser.delete()
                    await m.reply_text(f"🚫 ᴇʀʀᴏʀ: `{ep}`")

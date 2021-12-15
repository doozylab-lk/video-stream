from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from program import __version__
from driver.filters import command, other_filters
from pyrogram import Client, filters
from pyrogram import __version__ as pyrover
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""✨ **ᴡᴇʟᴄᴏᴍᴇ {message.from_user.mention()} !**\n
💭 [{BOT_NAME}](https://t.me/{BOT_USERNAME}) **ᴛʜɪs ɪs ᴛʜᴇ ᴍᴏsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ ʙᴏᴛ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴠᴏɪᴄᴇ ᴄᴀʟʟ ᴇᴀsɪʟʏ🚸 & sᴀғᴇʟʏ ✅!**
💡 **ꜰɪɴᴅ ᴏᴜᴛ ᴀʟʟ ᴛʜᴇ ʙᴏᴛ'ꜱ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ ʜᴏᴡ ᴛʜᴇʏ ᴡᴏʀᴋ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴏɴ ᴛʜᴇ »  ᴄᴏᴍᴍᴀɴᴅꜱ ʙᴜᴛᴛᴏɴ!**
🔖 **ᴛᴏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ, ᴘʟᴇᴀꜱᴇ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ » ʙᴀꜱɪᴄ ɢᴜɪᴅᴇ ʙᴜᴛᴛᴏɴ!**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀᴇ ɢʀᴏᴜᴘ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("ʙᴀsɪᴄ ɢᴜɪᴅᴇ", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅs", callback_data="cbbasic"),
                    InlineKeyboardButton("ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "ɢʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ", url="https://github.com/doozylab-lk/video-stream"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )

@Client.on_message(
    command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def alive(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ɢʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton(
                    "ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )

    alive = f"**ʜᴇʟʟᴏ {message.from_user.mention()}, i'm {BOT_NAME}**\n\n✨ ʙᴏᴛ ɪꜱ ᴡᴏʀᴋɪɴɢ ɴᴏʀᴍᴀʟʟʏ\n🍀 ᴍʏ ᴍᴀꜱᴛᴇʀ: [{ALIVE_NAME}](https://t.me/{OWNER_NAME})\n✨ ʙᴏᴛ ᴠᴇʀꜱɪᴏɴ: `v{__version__}`\n🍀 ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀꜱɪᴏɴ: `{pyrover}`\n✨ ᴘʏᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ: `{__python_version__}`\n🍀 ᴘʏᴛɢᴄᴀʟʟꜱ ᴠᴇʀꜱɪᴏɴ: `{pytover.__version__}`\n✨ ᴜᴘᴛɪᴍᴇ ꜱᴛᴀᴛᴜꜱ: `{uptime}`\n\n**ᴛʜᴀɴᴋꜱ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ʜᴇʀᴇ, ꜰᴏʀ ᴘʟᴀʏɪɴɢ ᴠɪᴅᴇᴏ & ᴍᴜꜱɪᴄ ᴏɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ'ꜱ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ** ❤"

    await message.reply_photo(
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `PONG!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot status:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )

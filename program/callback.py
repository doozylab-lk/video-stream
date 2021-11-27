from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **ᴡᴇʟᴄᴏᴍᴇ [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**\n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) ᴀʟʟᴏᴡs ʏᴏᴜ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ ᴀɴᴅ ᴠɪᴅᴇᴏ ᴏɴ ɢʀᴏᴜᴘs ᴛʜʀᴏᴜɢʜ ᴛʜᴇ ɴᴇᴡ ᴛᴇʟᴇɢʀᴀᴍ's ᴠɪᴅᴇᴏ ᴄʜᴀᴛs!**

💡 **ғɪɴᴅ ᴏᴜᴛ ᴀʟʟ ᴛʜᴇ ʙᴏᴛ's ᴄᴏᴍᴍᴀɴᴅs ᴀɴᴅ ʜᴏᴡ ᴛʜᴇʏ ᴡᴏʀᴋ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴏɴ ᴛʜᴇ » 📚 ᴄᴏᴍᴍᴀɴᴅs ʙᴜᴛᴛᴏɴ!**

🔖 **ᴛᴏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ, ᴘʟᴇᴀsᴇ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ » ❓ ʙᴀsɪᴄ ɢᴜɪᴅᴇ ʙᴜᴛᴛᴏɴ!**""",
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

@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ **ʙᴀsɪᴄ ɢᴜɪᴅᴇ ғᴏʀ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ::**

𝟷.) **ғɪʀsᴛ, ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ.** 
𝟸.) **ᴛʜᴇɴ, ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ ᴀɴᴅ ɢɪᴠᴇ ᴀʟʟ ᴘᴇʀᴍɪssɪᴏɴs ᴇxᴄᴇᴘᴛ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ.** 
𝟹.) **ᴀғᴛᴇʀ ᴘʀᴏᴍᴏᴛɪɴɢ ᴍᴇ, ᴛʏᴘᴇ /reload ɪɴ ɢʀᴏᴜᴘ ᴛᴏ ʀᴇғʀᴇsʜ ᴛʜᴇ ᴀᴅᴍɪɴ ᴅᴀᴛᴀ.** 
𝟹.) **ᴀᴅᴅ @{ASSISTANT_NAME} ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴏʀ ᴛʏᴘᴇ /userbotjoin ᴛᴏ ɪɴᴠɪᴛᴇ ʜᴇʀ.** 
𝟺.) **ᴛᴜʀɴ ᴏɴ ᴛʜᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ғɪʀsᴛ ʙᴇғᴏʀᴇ sᴛᴀʀᴛ ᴛᴏ ᴘʟᴀʏ ᴠɪᴅᴇᴏ/ᴍᴜsɪᴄ.** 
𝟻.) **sᴏᴍᴇᴛɪᴍᴇs, ʀᴇʟᴏᴀᴅɪɴɢ ᴛʜᴇ ʙᴏᴛ ʙʏ ᴜsɪɴɢ /reload ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ғɪx sᴏᴍᴇ ᴘʀᴏʙʟᴇᴍ.**  

📌 **ɪғ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ɴᴏᴛ ᴊᴏɪɴᴇᴅ ᴛᴏ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ, ᴍᴀᴋᴇ sᴜʀᴇ ɪғ ᴛʜᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴀʟʀᴇᴀᴅʏ ᴛᴜʀɴᴇᴅ ᴏɴ, ᴏʀ ᴛʏᴘᴇ /userbotleave ᴛʜᴇɴ ᴛʏᴘᴇ /userbotjoin ᴀɢᴀɪɴ.**  

💡 **ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀ ғᴏʟʟᴏᴡ-ᴜᴘ ǫᴜᴇsᴛɪᴏɴs ᴀʙᴏᴜᴛ ᴛʜɪs ʙᴏᴛ, ʏᴏᴜ ᴄᴀɴ ᴛᴇʟʟ ɪᴛ ᴏɴ ᴍʏ sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ ʜᴇʀᴇ: @{GROUP_SUPPORT}**  

⚡__ᴘᴏᴡᴇʀᴇᴅ ʙʏ {BOT_NAME} __""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("«🔙ɢᴏ ʙᴀᴄᴋ", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Hello [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**

» **press the button below to read the explanation and see the list of available commands !**

⚡__ᴘᴏᴡᴇʀᴇᴅ ʙʏ {BOT_NAME} __""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("«ᴀᴅᴍɪɴ ᴄᴍᴅ»", callback_data="cbadmin"),
                    InlineKeyboardButton("«sᴜᴅᴏ ᴄᴍᴅ»", callback_data="cbsudo"),
                ],[                                       
                    InlineKeyboardButton("«ʙᴀsɪᴄ ᴄᴍᴅ»", callback_data="cbbasic")
                ],[
                    InlineKeyboardButton("«🔙ɢᴏ ʙᴀᴄᴋ»", callback_data="cbstart")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 here is the basic commands:

» /play (song name/link) - play music on video chat
» /stream (query/link) - stream the yt live/radio live music
» /vplay (video name/link) - play video on video chat
» /vstream - play live video from yt live/m3u8
» /playlist - show you the playlist
» /video (query) - download video from youtube
» /song (query) - download song from youtube
» /lyric (query) - scrap the song lyric
» /search (query) - search a youtube video link

» /ping - show the bot ping status
» /uptime - show the bot uptime status
» /alive - show the bot alive info (in group)

⚡__ᴘᴏᴡᴇʀᴇᴅ ʙʏ {BOT_NAME} __""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("«🔙ɢᴏ ʙᴀᴄᴋ", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 here is the admin commands:

» /pause - pause the stream
» /resume - resume the stream
» /skip - switch to next stream
» /stop - stop the streaming
» /vmute - mute the userbot on voice chat
» /vunmute - unmute the userbot on voice chat
» /volume `1-200` - adjust the volume of music (userbot must be admin)
» /reload - reload bot and refresh the admin data
» /userbotjoin - invite the userbot to join group
» /userbotleave - order userbot to leave from group

⚡__ᴘᴏᴡᴇʀᴇᴅ ʙʏ {BOT_NAME} __""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("«🔙ɢᴏ ʙᴀᴄᴋ", callback_data="cbcmds")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 here is the sudo commands:

» /rmw - clean all raw files
» /rmd - clean all downloaded files
» /leaveall - order userbot to leave from all group

⚡__ᴘᴏᴡᴇʀᴇᴅ ʙʏ {BOT_NAME} __""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("«🔙ɢᴏ ʙᴀᴄᴋ", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 only admin with manage voice chats permission that can tap this button !", show_alert=True)
    await query.edit_message_text(
        f"⚙️ {query.message.chat.title}\n\n⏸ : pause stream\n▶️ : resume stream\n⏹ : stop stream\n⏭️ : skip stream\n🔇 : mute userbot\n🔊 : unmute userbot",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("⏹", callback_data="cbstop"),
                InlineKeyboardButton("⏸", callback_data="cbpause"),
                InlineKeyboardButton("▶️", callback_data="cbresume"),
                InlineKeyboardButton("⏭️", callback_data="cbskip"),
            ],[
                InlineKeyboardButton("🔇", callback_data="cbmute"),
                InlineKeyboardButton("🔊", callback_data="cbunmute"),
            ],[
                InlineKeyboardButton("🗑 Close", callback_data="cls")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 only admin with manage voice chats permission that can tap this button !", show_alert=True)
    await query.message.delete()

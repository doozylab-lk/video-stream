from cache.admins import admins
from driver.doozy import call_py
from pyrogram import Client, filters
from driver.decorators import authorized_users_only
from driver.filters import command, other_filters
from driver.queues import QUEUE, clear_queue
from driver.utils import skip_current_song, skip_item
from config import BOT_USERNAME, GROUP_SUPPORT, IMG_3, UPDATES_CHANNEL
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


bttn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 ɢᴏ ʙᴀᴄᴋ", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup(
    [[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="cls")]]
)


@Client.on_message(command(["reload", f"reload@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ ʙᴏᴛ **ʀᴇʟᴏᴀᴅᴇᴅ ᴄᴏʀʀᴇᴄᴛʟʏ !**\n✅ **ᴀᴅᴍɪɴ ʟɪꜱᴛ** ʜᴀꜱ ʙᴇᴇɴ **ᴜᴘᴅᴀᴛᴇᴅ !**"
    )


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}", "vskip"]) & other_filters)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ᴍᴇɴᴜ", callback_data="cbmenu"
                ),
                InlineKeyboardButton(
                    text="ᴄʟᴏsᴇ", callback_data="cls"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("❌ ɴᴏᴛʜɪɴɢ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ᴘʟᴀʏɪɴɢ")
        elif op == 1:
            await m.reply("✅ __Qᴜᴇᴜᴇꜱ__ **ɪꜱ ᴇᴍᴘᴛʏ.**\n\n**• ᴜꜱᴇʀʙᴏᴛ ʟᴇᴀᴠɪɴɢ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ**")
        elif op == 2:
            await m.reply("🗑️ **ᴄʟᴇᴀʀɪɴɢ ᴛʜᴇ Qᴜᴇᴜᴇꜱ**\n\n**• ᴜꜱᴇʀʙᴏᴛ ʟᴇᴀᴠɪɴɢ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ**")
        else:
            await m.reply_photo(
                photo=f"{IMG_3}",
                caption=f"⏭ **ꜱᴋɪᴘᴘᴇᴅ ᴛᴏ ᴛʜᴇ ɴᴇxᴛ ᴛʀᴀᴄᴋ.**\n\n🏷 **Name:** [{op[0]}]({op[1]})\n💭 **Chat:** `{chat_id}`\n💡 **Status:** `Playing`\n🎧 **Request by:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **ʀᴇᴍᴏᴠᴇᴅ ꜱᴏɴɢ ꜰʀᴏᴍ Qᴜᴇᴜᴇ:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(
    command(["stop", f"stop@{BOT_USERNAME}", "end", f"end@{BOT_USERNAME}", "vstop"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("✅ **ꜱᴛʀᴇᴀᴍɪɴɢ ʜᴀꜱ ᴇɴᴅᴇᴅ.**")
        except Exception as e:
            await m.reply(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛʜɪɴɢ ɪɴ ꜱᴛʀᴇᴀᴍɪɴɢ**")


@Client.on_message(
    command(["pause", f"pause@{BOT_USERNAME}", "vpause"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "⏸ **ᴛʀᴀᴄᴋ ᴘᴀᴜꜱᴇᴅ.**\n\n• **ᴛᴏ ʀᴇꜱᴜᴍᴇ ᴛʜᴇ ꜱᴛʀᴇᴀᴍ, ᴜꜱᴇ ᴛʜᴇ**\n» /resume ᴄᴏᴍᴍᴀɴᴅ."
            )
        except Exception as e:
            await m.reply(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛʜɪɴɢ ɪɴ ꜱᴛʀᴇᴀᴍɪɴɢ**")


@Client.on_message(
    command(["resume", f"resume@{BOT_USERNAME}", "vresume"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "▶️ **ᴛʀᴀᴄᴋ ʀᴇꜱᴜᴍᴇᴅ.**\n\n• **ᴛᴏ ᴘᴀᴜꜱᴇ ᴛʜᴇ ꜱᴛʀᴇᴀᴍ, ᴜꜱᴇ ᴛʜᴇ**\n» /pause ᴄᴏᴍᴍᴀɴᴅ."
            )
        except Exception as e:
            await m.reply(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛʜɪɴɢ ɪɴ ꜱᴛʀᴇᴀᴍɪɴɢ**")


@Client.on_message(
    command(["mute", f"mute@{BOT_USERNAME}", "vmute"]) & other_filters
)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "🔇 **ᴜꜱᴇʀʙᴏᴛ ᴍᴜᴛᴇᴅ.**\n\n• **ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴛʜᴇ ᴜꜱᴇʀʙᴏᴛ, ᴜꜱᴇ ᴛʜᴇ**\n» /unmute ᴄᴏᴍᴍᴀɴᴅ."
            )
        except Exception as e:
            await m.reply(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛʜɪɴɢ ɪɴ ꜱᴛʀᴇᴀᴍɪɴɢ**")


@Client.on_message(
    command(["unmute", f"unmute@{BOT_USERNAME}", "vunmute"]) & other_filters
)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "🔊 **ᴜꜱᴇʀʙᴏᴛ ᴜɴᴍᴜᴛᴇᴅ.**\n\n• **ᴛᴏ ᴍᴜᴛᴇ ᴛʜᴇ ᴜꜱᴇʀʙᴏᴛ, ᴜꜱᴇ ᴛʜᴇ**\n» /mute ᴄᴏᴍᴍᴀɴᴅ."
            )
        except Exception as e:
            await m.reply(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛʜɪɴɢ ɪɴ ꜱᴛʀᴇᴀᴍɪɴɢ**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("ʏᴏᴜ'ʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ !\n\nʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜꜱᴇʀ ᴀᴄᴄᴏᴜɴᴛ ꜰʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 ᴏɴʟʏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛꜱ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛʜᴀᴛ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪꜱ ʙᴜᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text(
                "⏸ ᴛʜᴇ ꜱᴛʀᴇᴀᴍɪɴɢ ʜᴀꜱ ᴘᴀᴜꜱᴇᴅ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ꜱᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("ʏᴏᴜ'ʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ !\n\nʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜꜱᴇʀ ᴀᴄᴄᴏᴜɴᴛ ꜰʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 ᴏɴʟʏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛꜱ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛʜᴀᴛ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪꜱ ʙᴜᴛᴛᴏɴ!", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "▶️ ᴛʜᴇ ꜱᴛʀᴇᴀᴍɪɴɢ ʜᴀꜱ ʀᴇꜱᴜᴍᴇᴅ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ꜱᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("ʏᴏᴜ'ʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ !\n\nʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜꜱᴇʀ ᴀᴄᴄᴏᴜɴᴛ ꜰʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 ᴏɴʟʏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛꜱ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛʜᴀᴛ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪꜱ ʙᴜᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("✅ **ᴛʜɪꜱ ꜱᴛʀᴇᴀᴍɪɴɢ ʜᴀꜱ ᴇɴᴅᴇᴅ**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ꜱᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("ʏᴏᴜ'ʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ !\n\nʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜꜱᴇʀ ᴀᴄᴄᴏᴜɴᴛ ꜰʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 ᴏɴʟʏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛꜱ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛʜᴀᴛ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪꜱ ʙᴜᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "🔇 ᴜꜱᴇʀʙᴏᴛ ꜱᴜᴄᴄᴇꜱꜰᴜʟʟʏ ᴍᴜᴛᴇᴅ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ꜱᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("ʏᴏᴜ'ʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ !\n\nʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜꜱᴇʀ ᴀᴄᴄᴏᴜɴᴛ ꜰʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 ᴏɴʟʏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛꜱ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛʜᴀᴛ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪꜱ ʙᴜᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "🔊 ᴜꜱᴇʀʙᴏᴛ ꜱᴜᴄᴄᴇꜱꜰᴜʟʟʏ ᴜɴᴍᴜᴛᴇᴅ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ꜱᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"✅ **ᴠᴏʟᴜᴍᴇ ꜱᴇᴛ ᴛᴏ** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛʜɪɴɢ ɪꜱ ꜱᴛʀᴇᴀᴍɪɴɢ**")

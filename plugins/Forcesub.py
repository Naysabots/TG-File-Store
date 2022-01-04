import os
from pyrogram import Client, filters
OWNER_ID = os.environ.get('OWNER_ID')
UPDATES_CHANNEL = os.environ.get('UPDATES_CHANNEL', '')
DB_CHANNEL_ID = os.environ.get("DB_CHANNEL_ID")
from config import *
# (c) @AbirHasan2005

import asyncio
from typing import union
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


async def get_invite_link(bot: Client, chat_id: Union[str, int]):
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=chat_id)
        return invite_link
    except FloodWait as e:
        print(f"Sleep of {e.x}s caused by FloodWait ...")
        await asyncio.sleep(e.x)
        return await get_invite_link(bot, chat_id)


async def handle_force_sub(bot: Client, cmd: Message):
    if UPDATES_CHANNEL and UPDATES_CHANNEL.startswith("-100"):
        channel_chat_id = int(UPDATES_CHANNEL)
    elif UPDATES_CHANNEL and (not UPDATES_CHANNEL.startswith("-100")):
        channel_chat_id = Config.UPDATES_CHANNEL
    else:
        return 200
    try:
        user = await bot.get_chat_member(chat_id=channel_chat_id, user_id=cmd.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=cmd.from_user.id,
                text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/JoinOT).",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return 400
    except UserNotParticipant:
        try:
            invite_link = await get_invite_link(bot, chat_id=channel_chat_id)
        except Exception as err:
            print(f"Unable to do Force Subscribe to {Config.UPDATES_CHANNEL}\n\nError: {err}")
            return 200
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**\n\n"
                 "Due to Overload, Only Channel Subscribers can use the Bot!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                    ],
                    [
                        InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshForceSub")
                    ]
                ]
            ),
            parse_mode="markdown"
        )
        return 400
    except Exception:
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="Something went Wrong. Contact my [Support Group](https://t.me/JoinOT).",
            parse_mode="markdown",
            disable_web_page_preview=True
        )
        return 200
    return 200




@Client.on_callback_query(filters.regex('refreshForceSub'))
async def refresh_cb(c, m):
    owner = await c.get_users(int(OWNER_ID))
    if UPDATE_CHANNEL:
        try:
            user = await c.get_chat_member(UPDATE_CHANNEL, m.from_user.id)
            if user.status == "kicked":
               try:
                   await m.message.edit("**Hey you are banned 😜**")
               except:
                   pass
               return
        except UserNotParticipant:
            await m.answer('You are not yet joined our channel. First join and then press refresh button 🤤', show_alert=True)
            return
        except Exception as e:
            print(e)
            await m.message.edit(f"Something Wrong. Please try again later or contact {owner.mention(style='md')}")
            return

    cmd, chat_id, msg_id = m.data.split("+")
    msg = await c.get_messages(int(chat_id), int(msg_id)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(msg_id))

    if msg.empty:
        return await m.reply_text(f"🥴 Sorry bro your file was missing\n\nPlease contact my owner 👉 {owner.mention(style='md')}")

    caption = msg.caption.markdown

    if chat_id.startswith('-100'): #if file from channel
        channel = await c.get_chat(int(chat_id))
        caption += "\n\n\n**--Uploader Details:--**\n\n"
        caption += f"__📢 Channel Name:__ `{channel.title}`\n\n"
        caption += f"__🗣 User Name:__ @{channel.username}\n\n" if channel.username else ""
        caption += f"__👤 Channel Id:__ `{channel.id}`\n\n"
        caption += f"__💬 DC ID:__ {channel.dc_id}\n\n" if channel.dc_id else ""
        caption += f"__👁 Members Count:__ {channel.members_count}\n\n" if channel.members_count else ""

    else: #if file not from channel
        user = await c.get_users(int(chat_id))
        caption += "\n\n\n**--Uploader Details:--**\n\n"
        caption += f"__🦚 First Name:__ `{user.first_name}`\n\n"
        caption += f"__🐧 Last Name:__ `{user.last_name}`\n\n" if user.last_name else ""
        caption += f"__👁 User Name:__ @{user.username}\n\n" if user.username else ""
        caption += f"__👤 User Id:__ `{user.id}`\n\n"
        caption += f"__💬 DC ID:__ {user.dc_id}\n\n" if user.dc_id else ""

    await msg.copy(m.from_user.id, caption=caption)
    await m.message.delete()

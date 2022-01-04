import os
import asyncio
import logging
import logging.config
from plugins.database.database import db
from pyrogram.types import Message
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from config import *
import base64
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ListenerCanceled
DB_CHANNEL_ID = os.environ.get("DB_CHANNEL_ID")
OWNER_ID = os.environ.get("OWNER_ID")
BATCH = []
from plugins.Forcesub import (
    handle_force_sub,
    get_invite_link
)

from plugins.database.adduser import add_user_to_database
@Client.on_message(filters.private & filters.command(["start"]))
async def help_user(bot, cmd, cb=false):
    # logger.info(update)
    await AddUser(bot, cmd)

    if not cb:
        send_msg = await cmd.reply_text("**Processing...**", quote=True)

    owner = await bot.get_users(int(OWNER_ID))
    owner_username = owner.username if owner.username else 'Ns_bot_updates'

    
    text = f"""Hey! {cmd.from_user.mention(style='md')}

** I am Telegram File Store Bot**

`You can store your Telegram Media for permanent Link!`

`No Channel Forcesub Added.`

**👲 Maintained By** @DKBOTZ
"""

    # Buttons
    buttons = [
        [
            InlineKeyboardButton('My Father 👨‍✈️', url=f"https://t.me/{owner_username}"),
            InlineKeyboardButton('Help 💡', callback_data="help")
        ],
        [
            InlineKeyboardButton('About 📕', callback_data="about")
        ]
    ]

    # when button home is pressed
    if cb:
        return await cmd.message.edit(
                   text=text,
                   reply_markup=InlineKeyboardMarkup(buttons)
               )

    if len(cmd.command) > 1: # sending the stored file
        try:
            cmd.command[1] = await decode(cmd.command[1])
        except:
            pass

        if 'batch_' in cmd.command[1]:
            await send_msg.delete()
            cmd, chat_id, message = cmd.command[1].split('_')
            string = await cmd.get_messages(int(chat_id), int(message)) if not DB_CHANNEL_ID else await bot.get_messages(int(DB_CHANNEL_ID), int(message))

            if string.empty:
                owner = await bot.get_users(int(OWNER_ID))
                return await cmd.reply_text(f"🥴 Sorry bro your file was deleted by file owner or bot owner\n\nFor more help contact my owner 👉 {owner.mention(style='md')}")
            message_ids = (await decode(string.text)).split('-')
            for msg_id in message_ids:
                msg = await bot.get_messages(int(chat_id), int(msg_id)) if not DB_CHANNEL_ID else await bot.get_messages(int(DB_CHANNEL_ID), int(msg_id))

                if msg.empty:
                    owner = await bot.get_users(int(OWNER_ID))
                    return await cmd.reply_text(f"🥴 Sorry bro your file was deleted by file owner or bot owner\n\nFor more help contact my owner 👉 {owner.mention(style='md')}")

                await msg.copy(m.from_user.id)
                await asyncio.sleep(0)
            return

        chat_id, msg_id = cmd.command[1].split('_')
        msg = await bot.get_messages(int(chat_id), int(msg_id)) if not DB_CHANNEL_ID else await bot.get_messages(int(DB_CHANNEL_ID), int(msg_id))

        if msg.empty:
            return await send_msg.edit(f"🥴 Sorry bro your file was deleted by file owner or bot owner\n\nFor more help contact my owner 👉 {owner.mention(style='md')}")
        
        caption = f"{msg.caption.markdown}" if msg.caption else ""
        await send_msg.delete()
        await msg.copy(cmd.from_user.id, caption=caption)


    else: # sending start message
        await send_msg.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

@Client.on_message(filters.command('me') & filters.incoming & filters.private)
async def me(c, m):


    """ This will be sent when /me command was used"""

    me = await c.get_users(m.from_user.id)
    text = "--**YOUR DETAILS:**--\n\n\n"
    text += f"__🦚 First Name:__ `{me.first_name}`\n\n"
    text += f"__🐧 Last Name:__ `{me.last_name}`\n\n" if me.last_name else ""
    text += f"__👁 User Name:__ @{me.username}\n\n" if me.username else ""
    text += f"__👤 User Id:__ `{me.id}`\n\n"
    text += f"__💬 DC ID:__ {me.dc_id}\n\n" if me.dc_id else ""
    text += f"__✔ Is Verified By TELEGRAM:__ `{me.is_verified}`\n\n" if me.is_verified else ""
    text += f"__👺 Is Fake:__ {me.is_fake}\n\n" if me.is_fake else ""
    text += f"__💨 Is Scam:__ {me.is_scam}\n\n" if me.is_scam else ""
    text += f"__📃 Language Code:__ {me.language_code}\n\n" if me.language_code else ""

    await m.reply_text(text, quote=True)

@Client.on_message(filters.command('batch') & filters.private & filters.incoming)
async def batch(c, m):

    
    """ This is for batch command"""

    BATCH.append(m.from_user.id)
    files = []
    i = 1

    while m.from_user.id in BATCH:
        if i == 1:
            media = await c.ask(chat_id=m.from_user.id, text='Send me some files or videos or photos or text or audio. If you want to cancel the process send /cancel')
            if media.text == "/cancel":
                return await m.reply_text('Cancelled Successfully ✌')
            files.append(media)
        else:
            try:
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Done ✅', callback_data='done')]])
                media = await c.ask(chat_id=m.from_user.id, text='Ok 😉. Now send me some more files Or press done to get shareable link. If you want to cancel the process send /cancel', reply_markup=reply_markup)
                if media.text == "/cancel":
                    return await m.reply_text('Cancelled Successfully ✌')
                files.append(media)
            except ListenerCanceled:
                pass
            except Exception as e:
                print(e)
                await m.reply_text(text="Something went wrong. Try again later.")
        i += 1

    message = await m.reply_text("Generating shareable link 🔗")
    string = ""
    for file in files:
        if DB_CHANNEL_ID:
            copy_message = await file.copy(int(DB_CHANNEL_ID))
        else:
            copy_message = await file.copy(m.from_user.id)
        string += f"{copy_message.message_id}-"
        await asyncio.sleep(1)

    string_base64 = await encode_string(string[:-1])
    send = await c.send_message(m.from_user.id, string_base64) if not DB_CHANNEL_ID else await c.send_message(int(DB_CHANNEL_ID), string_base64)
    base64_string = await encode_string(f"batch_{m.chat.id}_{send.message_id}")
    bot = await c.get_me()
    url = f"https://t.me/{BOT_USERNAME}?start={base64_string}"

    await message.edit(text=url)


async def decode(base64_string):
    base64_bytes = base64_string.encode("ascii")
    string_bytes = base64.b64decode(base64_bytes) 
    string = string_bytes.decode("ascii")
    return string

async def encode_string(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


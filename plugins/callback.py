import os
import logging
import logging.config

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from config import *
from .commands import BATCH, start
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
DB_CHANNEL_ID = os.environ.get("DB_CHANNEL_ID")
OWNER_ID = os.environ.get("OWNER_ID")


@Client.on_callback_query(filters.regex('^homes$'))
async def homes_cb(c, m):
    await m.answer()

    # help text
    help_text = """Hey User

**I am Telegram File Store Bot**

`You can store your Telegram Media for permanent Link!`

**👲 Maintained By** @Tellybots_4u
"""

    # creating buttons
    buttons = [
                 [InlineKeyboardButton("Channel", url="https://t.me/Tellybots"),
                  InlineKeyboardButton("Support", url="https://t.me/Tellybots_support")],
                 [InlineKeyboardButton("Help", callback_data="help"),
                  InlineKeyboardButton("About", callback_data="about")],
                 [InlineKeyboardButton("🔐 Close", callback_data="close")]
                ]

    # editing as help message
    await m.message.edit(
        text=help_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_callback_query(filters.regex('^help$'))
async def help_cb(c, m):
    await m.answer()

    # help text
    help_text = """**You need Help?? 🧐**

★ Just send me the files i will store file and give you share able link


**You can use me in channel too 😉**

★ Make me admin in your channel with edit permission. Thats enough now continue uploading files in channel i will edit all posts and add share able link url buttons"""

    # creating buttons
    buttons = [
        [
            InlineKeyboardButton('Home 🏕', callback_data='homes'),
            InlineKeyboardButton('About 📕', callback_data='about')
        ],
        [
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]
    ]

    # editing as help message
    await m.message.edit(
        text=help_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex('^close$'))
async def close_cb(c, m):
    await m.message.delete()
    await m.message.reply_to_message.delete()


@Client.on_callback_query(filters.regex('^about$'))
async def about_cb(c, m):
    await m.answer()
    owner = await c.get_users(int(OWNER_ID))
    bot = await c.get_me()

    # about text
    about_text = f"""--**My Details:**--

🤖 𝐌𝐲 𝐍𝐚𝐦𝐞: {bot.mention(style='md')}
    
📝 𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞: [Python 3](https://www.python.org/)

🧰 𝐅𝐫𝐚𝐦𝐞𝐰𝐨𝐫𝐤: [Pyrogram](https://github.com/pyrogram/pyrogram)

👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: {owner.mention(style='md')}

📢 𝐂𝐡𝐚𝐧𝐧𝐞𝐥: [Tellybots](https://t.me/tellybots_4u)

"""

    # creating buttons
    buttons = [
        [
            InlineKeyboardButton('Home 🏕', callback_data='home'),
            InlineKeyboardButton('Help 💡', callback_data='help')
        ],
        [
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]
    ]

    # editing message
    await m.message.edit(
        text=about_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex('^home$'))
async def home_cb(c, m):
    await m.answer()
    await start(c, m, cb=True)


@Client.on_callback_query(filters.regex('^done$'))
async def done_cb(c, m):
    BATCH.remove(m.from_user.id)
    c.cancel_listener(m.from_user.id)
    await m.message.delete()


@Client.on_callback_query(filters.regex('^delete'))
async def delete_cb(c, m):
    await m.answer()
    cmd, msg_id = m.data.split("+")
    chat_id = m.from_user.id if not DB_CHANNEL_ID else int(DB_CHANNEL_ID)
    message = await c.get_messages(chat_id, int(msg_id))
    await message.delete()
    await m.message.edit("Deleted files successfully 👨‍✈️")

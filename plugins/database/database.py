from pyrogram.types import Message
from pyrogram import Client as Tellybots
from pyrogram import filters
from config import *
from plugins.database.adduser import present_in_userbase, add_to_userbase, get_users # userbase.py is Attached below
import time

@Tellybots.on_message(filters.private & filters.command('broadcast') & filters.user(OWNER_ID) & filters.reply)

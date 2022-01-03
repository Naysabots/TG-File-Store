import traceback
import os

from pyrogram import Client as Tellybots
from pyrogram import filters
from config import *

from plugins.database.access import tellybots

@Tellybots.on_message(filters.private & filters.command('stats'))
async def sts(c, m):
    if m.from_user.id != OWNER_ID:
        return 
    total_users = await tellybots.total_users_count()
    await m.reply_text(text=f"Total

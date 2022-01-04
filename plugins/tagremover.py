import os
from pyrogram import Client as dkbotz, filters




@dkbotz.on_message(filters.forwarded)
async def forward(bot, message):
    await message.delete()

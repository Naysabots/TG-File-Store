# (c) @AbirHasan2005


from pyrogram import Client
from plugins.database.access import tellybots
from pyrogram.types import Message


async def add_user_to_database(bot: Client, update: Message):
    if not await tellybots.is_user_exist(update.from_user.id):
           await tellybots.add_user(update.from_user.id)

 

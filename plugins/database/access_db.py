from config import *
from plugins.database.database import Database

db = Database(DATABASE_URL, BOT_USERNAME)

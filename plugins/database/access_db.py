from configs import Config
from plugins.database.database import Database

db = Database(Config.MONGODB_URI, Config.BOT_USERNAME)

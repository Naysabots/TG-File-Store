
from config import *
from plugins.database.database import Database

tellybots = Database(MONGODB_URL, SESSION_NAME)

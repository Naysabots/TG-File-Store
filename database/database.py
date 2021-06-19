from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import os
import threading
import asyncio

from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, UniqueConstraint, func

DATABASE_URL = os.environ.get("DATABASE_URL", "")

def start() -> scoped_session:
    engine = create_engine(DATABASE_URL, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))

BASE = declarative_base()
SESSION = start()

INSERTION_LOCK = threading.RLock()

class Database(BASE):
    __tablename__ = "database"
    id = Column(Integer, primary_key=True)
    up_name = Column(Boolean)

    def __init__(self, id, up_name):
        self.id = id
        self.up_name = up_name

Database.__table__.create(checkfirst=True)

async def update_as_name(id, mode):
    with INSERTION_LOCK:
        msg = SESSION.query(Database).get(id)
        if not msg:
            msg = Database(id, True)
        else:
            msg.up_name = mode
            SESSION.delete(msg)
        SESSION.add(msg)
        SESSION.commit()

async def get_data(id):
    try:
        user_data = SESSION.query(Database).get(id)
        if not user_data:
            new_user = Database(id, True)
            SESSION.add(new_user)
            SESSION.commit()
            user_data = SESSION.query(Database).get(id)
        return user_data
    finally:
        SESSION.close()


class CDatabase(BASE):
    # for storing encoded id, Uploader data !!
    __tablename__ = "cdatabase"
    msg_cal = Column(String,primary_key=True)
    msg_updata = Column(String)

    def __init__(self, msg_cal,msg_updata):
        self.msg_cal = msg_cal
        self.msg_updata = msg_updata

CDatabase.__table__.create(checkfirst=True)

async def add_updata(msg_cal,msg_updata):
    with INSERTION_LOCK:
        msg = CDatabase(msg_cal,msg_updata)
        SESSION.add(msg)
        SESSION.commit()
        
async def get_updata(msg_cal):
    try:
       user_updata= SESSION.query(CDatabase).get(msg_cal)
       if not user_updata:
           return ""
       return user_updata.msg_updata
       # direct gib that uploaders details !!
    
    finally:
       SESSION.close()

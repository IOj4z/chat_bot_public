from sqlalchemy import Column, BigInteger, String,TIMESTAMP, sql

from utils.db_api.db_jelebot import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    tg_user_id = Column(String(200), primary_key=True)
    id = Column(String(200))
    first_name = Column(String(200))
    last_name = Column(String(200))
    corporation = Column(String(200))
    about = Column(String(200))
    tg_first_name = Column(String(200))
    tg_username = Column(String(200))
    status = Column(String(30))
    address = Column(String(30))
    avatar = Column(String(30))
    what = Column(String(200))
    why = Column(String(200))
    moderator = Column(BigInteger)
    deleted_at = Column(TIMESTAMP)

    query: sql.select

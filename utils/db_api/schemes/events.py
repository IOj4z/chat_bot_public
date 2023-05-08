from sqlalchemy import Column, BigInteger, String,TIMESTAMP, sql

from utils.db_api.db_jelebot import TimedBaseModel


class Events(TimedBaseModel):
    __tablename__ = 'events'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255))
    desc = Column(String(200))
    program = Column(String(200))
    speakers_id = Column(BigInteger)
    date = Column(String(200))
    cover = Column(String(200))
    user_id = Column(BigInteger)
    created_at = Column(String(200))
    deleted_at = Column(TIMESTAMP)

    query: sql.select

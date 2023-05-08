from sqlalchemy import Column, BigInteger,TIMESTAMP, String, sql

from utils.db_api.db_jelebot import TimedBaseModel


class EventsModerators(TimedBaseModel):
    __tablename__ = 'events_moderators'
    id = Column(BigInteger, primary_key=True)
    events_id = Column(BigInteger)
    users_id = Column(BigInteger)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)

    query: sql.select

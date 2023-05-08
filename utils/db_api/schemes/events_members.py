from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_jelebot import TimedBaseModel


class EventsMembers(TimedBaseModel):
    __tablename__ = 'events_members'
    id = Column(BigInteger, primary_key=True)
    events_id = Column(BigInteger)
    members_id = Column(BigInteger)
    in_person = Column(BigInteger)

    query: sql.select

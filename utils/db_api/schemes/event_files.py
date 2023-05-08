from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_jelebot import TimedBaseModel


class EventsFiles(TimedBaseModel):
    __tablename__ = 'events_files'
    id = Column(BigInteger, primary_key=True)
    events_id = Column(BigInteger)
    files_id = Column(BigInteger)

    query: sql.select

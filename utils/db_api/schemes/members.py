from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_jelebot import TimedBaseModel


class Members(TimedBaseModel):
    __tablename__ = 'members'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)

    query: sql.select

from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_jelebot import TimedBaseModel


class Moderator(TimedBaseModel):
    __tablename__ = 'moderators'
    id = Column(BigInteger, primary_key=True)
    code_activation = Column(String(60))
    status = Column(BigInteger)
    user_id = Column(BigInteger)

    query: sql.select

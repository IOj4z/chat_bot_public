from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_jelebot import TimedBaseModel


class Files(TimedBaseModel):
    __tablename__ = 'files'
    id = Column(BigInteger, primary_key=True)
    path = Column(String(255))

    query: sql.select

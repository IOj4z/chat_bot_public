from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_jelebot import TimedBaseModel


class Requests(TimedBaseModel):
    __tablename__ = 'requests'
    id = Column(BigInteger, primary_key=True)
    member_id = Column(String(200))
    send_request = Column(String(200))
    get_response = Column(String(200))
    to_member_id = Column(String(200))
    created_at = Column(String(200))
    updated_at = Column(String(200))

    query: sql.select

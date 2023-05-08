from asyncpg import UniqueViolationError
from utils.db_api.schemes.requests import Requests


async def add_request(member_id: str, send_request: int, get_response: int, to_member_id: str):
    try:
        request = Requests(

            member_id=member_id,
            send_request=send_request,
            get_response=get_response,
            to_member_id=to_member_id,
        )

        await request.create()
    except UniqueViolationError as ex:
        print('Запрос не выполнене')
        print(ex)
        return


async def check_exist_networking(member_id: str, to_member_id: str):
    try:
        requests = await Requests.query.where(
            Requests.member_id == member_id and Requests.to_member_id == to_member_id
        ).where(Requests.get_response == 1).gino.first()
        return requests
    except Exception as ex:
        print(ex)

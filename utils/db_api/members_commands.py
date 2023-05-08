from utils.db_api.db_jelebot import db
from utils.db_api.schemes.events import Events
from utils.db_api.schemes.members import Members


async def add_member(user_id: int):
    try:
        member = Members(
            user_id=user_id,
        )
        return await member.create()
    except Exception as ex:
        print('Участник не добавлен')
        print(ex)
        return


async def select_user_id(user_id):
    members = await Members.query.where(Members.user_id == user_id).gino.first()
    print(members)
    if members is None:
        return await add_member(int(user_id))
    return members


async def select_members(id):
    members = await Members.query.where(Members.id == id).gino.first()
    return members


async def select_all_members():
    members = await Members.query.gino.all()
    return members

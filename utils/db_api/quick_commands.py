from asyncpg import UniqueViolationError

from utils.db_api.db_jelebot import db
from utils.db_api.schemes.user import User


async def add_user(user_id: str, first_name: str, last_name: str, tg_first_name: str, corporation: str, about: str,
                   username: str, status: str, avatar: str, address: str):
    try:
        user = User(

            first_name=first_name,
            last_name=last_name,
            corporation=corporation,
            about=about,
            tg_user_id=str(user_id),
            tg_first_name=tg_first_name,
            tg_username=username,
            status=status,
            address=address,
            avatar=avatar)

        await user.create()
    except UniqueViolationError as ex:
        print('Пользовател не добавлен')
        print(ex)
        return


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count


async def select_user(user_id):
    user = await User.query.where(User.tg_user_id == str(user_id)).gino.first()
    if user.deleted_at:
        return None
    return user


async def select_user_id(tg_user_id):
    user = await User.query.where(User.tg_user_id == str(tg_user_id)).gino.first()
    return user


async def select_id(ids):
    user = await User.query.where(User.id == ids).gino.first()
    return user


async def update_user_status(user_id, status):
    user = await select_user(user_id)
    await user.update(status=status).apply()


async def update_user_first_name(user_id, first_name):
    user = await select_user(user_id)
    await user.update(first_name=first_name).apply()


async def update_user_last_name(user_id, last_name):
    user = await select_user(user_id)
    await user.update(last_name=last_name).apply()


async def update_user_about(user_id, about):
    user = await select_user(user_id)
    await user.update(about=about).apply()


async def update_user_avatar(user_id, avatar):
    user = await select_user(user_id)
    await user.update(avatar=avatar).apply()


async def update_user_corporation(user_id, corporation):
    user = await select_user(user_id)
    await user.update(corporation=corporation).apply()


async def update_user_what(user_id, what):
    user = await select_user(user_id)
    await user.update(what=what).apply()


async def update_user_why(user_id, why):
    user = await select_user(user_id)
    await user.update(why=why).apply()

from asyncpg import UniqueViolationError

from utils.db_api.db_jelebot import db
from utils.db_api.events_files import add_events_files
from utils.db_api.files_command import add_files
from utils.db_api.moderator_commands import add_events_moderators
from utils.db_api.schemes.events import Events


async def select_all_events():
    events = await Events.query.gino.all()

    return events


async def count_events():
    count = await db.func.count(Events.id).gino.scalar()
    return count


async def select_event(event_id):
    events = await Events.query.where(Events.id == event_id).gino.first()
    return events


async def add_events(name: str, desc: str, program: str, cover: str, date: str, file: str, user_id: int):
    try:
        event = Events(
            name=name,
            desc=desc,
            program=program,
            date=date,
            cover=cover,
            user_id=user_id,
        )

        events_id = await event.create()
        await add_events_moderators(user_id, events_id.id)
        file_id = await add_files(file)

        await add_events_files(file_id.id, events_id.id)
    except UniqueViolationError as ex:
        print('Мероприятие не добавлен')
        print(ex)
        return


async def update_event_name(event_id, name):
    event = await select_event(event_id)
    await event.update(name=name).apply()

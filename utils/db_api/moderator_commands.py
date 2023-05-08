from utils.db_api.schemes.moderator import Moderator
from utils.db_api.schemes.events import Events
from utils.db_api.schemes.moderators_events import EventsModerators


async def add_to_moderator(user_id: int):
    try:
        member = Moderator(
            user_id=user_id,
            status=0,
        )
        return await member.create()
    except Exception as ex:
        print(ex)
        return


async def add_events_moderators(user_id: int, event_id: int):
    try:
        event_member = EventsModerators(
            users_id=user_id,
            events_id=event_id,
        )
        await event_member.create()
    except Exception as ex:
        print(ex)
        return


async def check_status(id):
    members = await Moderator.query.where(Moderator.id == id).gino.first()

    return members


async def select_all_my_events(users_id):
    events = await EventsModerators.query.where(EventsModerators.users_id == users_id).gino.all()

    return events


async def select_my_events(events_id):
    event = await EventsModerators.query.where(EventsModerators.events_id == events_id).gino.first()
    return event


async def update_my_event_name(value, event_id):
    event = await select_my_events(event_id)
    await event.update(name=value).apply()


async def update_my_event_desc(value, event_id):
    event = await select_my_events(event_id)
    await event.update(desc=value).apply()


async def update_my_event_cover(value, event_id):
    event = await select_my_events(event_id)
    await event.update(cover=value).apply()


async def update_my_event_date(value, event_id):
    event = await select_my_events(event_id)
    await event.update(date=value).apply()


async def update_my_event_program(value, event_id):
    event = await select_my_events(event_id)
    await event.update(program=value).apply()

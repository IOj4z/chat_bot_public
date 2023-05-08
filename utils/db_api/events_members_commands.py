
from utils.db_api.schemes.events_members import EventsMembers


async def add_event_member(events_id: int, members_id: int, in_person: int):
    try:

        event_member = EventsMembers(
            events_id=events_id,
            members_id=members_id,
            in_person=in_person,
        )

        exist = await select_event_member(events_id, members_id, in_person)

        if not exist:
            return await event_member.create()
        else:
            return exist

    except Exception as ex:
        print(ex)
        print('Участник в мероприятие не добавлен')
        return


async def select_event_member(event_id, member_id, in_person):
    members = await EventsMembers.query.where(
        EventsMembers.members_id == member_id and EventsMembers.events_id == event_id,
    ).gino.all()
    return members


async def select_all_members(event_id):
    members = await EventsMembers.query.where(
        EventsMembers.events_id == event_id
    ).gino.all()
    return members


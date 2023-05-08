import asyncio

from data import config
from utils.db_api import quick_commands as commands
from utils.db_api import event_commands
from utils.db_api.db_jelebot import db


async def db_test():
    await db.set_bind(config.POSTGRES_URL)
    # await db.gino.drop_all()
    await db.gino.create_all()

    # await commands.add_user(1, 'Alex',)
    # await commands.add_user(34566, 'John')
    # await commands.add_user(342, 'bot')
    # await commands.add_user(4543, 'Alex')

    # users = await commands.select_all_users()
    events = await event_commands.select_all_events()
    for event in events:
        print(event.name)
    # print(events)
    #
    # count = await commands.count_users()
    # print(count)
    count = await event_commands.count_events()
    print(count)
    bcountut = await event_commands.select_all_events_as_button()
    print(bcountut)
    print(type(bcountut))

    events = await event_commands.select_event(2)
    print(events)
    #
    # user = await commands.select_user(1)
    # print(user)
    #
    # await commands.update_user_name(1, 'New Alex Name')
    # user = await commands.select_user(1)
    # print(user)


loop = asyncio.get_event_loop()
loop.run_until_complete(db_test())

from aiogram.dispatcher.filters.state import StatesGroup, State


class register(StatesGroup):
    address = State()
    avatar = State()
    tg_user_id = State()
    first_name = State()
    last_name = State()
    corporation = State()
    about = State()
    tg_first_name = State()
    tg_username = State()
    why = State()
    what = State()


class edit_state(StatesGroup):
    tg_user_id = State()
    first_name = State()
    last_name = State()
    corporation = State()
    about = State()
    tg_first_name = State()
    tg_username = State()
    address = State()
    avatar = State()
    why = State()
    what = State()


class events(StatesGroup):
    id = State()
    name = State()
    desc = State()
    date = State()
    cover = State()
    program = State()
    file = State()


class edit_sevents(StatesGroup):
    id = State()
    name = State()
    desc = State()
    program = State()
    date = State()
    cover = State()

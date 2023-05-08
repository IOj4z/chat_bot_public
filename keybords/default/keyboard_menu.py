from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.db_api.quick_commands import select_user_id


async def kb_menus(user_id):
    user = await select_user_id(user_id)
    if user.deleted_at:
        return None
    if user.moderator == 1:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Мой профиль'),
                    KeyboardButton(text='Редактировать'),
                ],
                [
                    KeyboardButton(text='Нетворкинг'),
                    KeyboardButton(text='Создать мероприятие'),
                    KeyboardButton(text='Мои мероприятия'),
                ],
                [
                    KeyboardButton(text='Прошедшие мероприятия'),
                    KeyboardButton(text='Будущие мероприятия'),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Мой профиль'),
                    KeyboardButton(text='Редактировать'),
                ],
                [
                    KeyboardButton(text='Нетворкинг'),
                    KeyboardButton(text='Стать модератором'),
                ],
                [
                    KeyboardButton(text='Прошедшие мероприятия'),
                    KeyboardButton(text='Будущие мероприятия'),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )


kb_test = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/menu'),
        ],

    ],
    resize_keyboard=True
)
kb_register = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Указать информацию'),
        ],
        [
            KeyboardButton(text='Отменить'),
        ],

    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

kb_moderator = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Указать информацию'),
        ],
        [
            KeyboardButton(text='Отменить'),
        ],

    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
kb_networking = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/Нэтворкинг'),
        ],

    ],
    resize_keyboard=True
)
kb_file = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/Файл'),
        ],

    ],
    resize_keyboard=True)

kb_all_events = ReplyKeyboardMarkup(

    keyboard=[
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

kb_cancel = ReplyKeyboardMarkup(

    keyboard=[
        [
            KeyboardButton(text='Отменить'),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

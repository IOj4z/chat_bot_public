import hashlib
import os

from keybords.inline import ikb_my
from loader import dp
from filters import IsPrivate
from aiogram import types
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton

from utils.db_api.moderator_commands import select_my_events
from utils.misc import rate_limit

from keybords.default import kb_register, kb_menus
from keybords.inline.inline_kb_events import ikb_last, ikb_future
from keybords.inline.inline_kb_networking import ikb_mem_networking
from keybords.inline.inline_kb_profile import ikb_profile_edit

from utils.db_api.quick_commands import select_all_users, select_id

from utils.db_api import quick_commands as commands
from utils.db_api import event_commands as events


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    try:
        user = await commands.select_user(message.from_user.id)

        if user.status == 'active':
            await message.answer(
                f"Привет {user.first_name}!\n")
        elif user.status == 'baned':
            await message.answer('Ты забанен')
    except Exception as ex:

        print(ex)
        await message.answer(
            f"Привет! Это чат - бот для мероприятий КБ - 12. Он поможет тебе:\n"
            f"в быстром и удобном установлении связей и нетворкинга\n"
            f"в быстрой регистрации на ивенты КБ - 12\n"
            f"в коммуникации с организаторами и админами мероприятий")

        await message.answer(
            text="Необходимо указать информацию о себе",
            reply_markup=kb_register,
        )


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/ban')
async def get_ban(message: Message):
    await commands.update_user_status(user_id=message.from_user.id, status='baned')
    await message.answer('Мы тебя забанели.')


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/unban')
async def get_unban(message: Message):
    await commands.update_user_status(user_id=message.from_user.id, status='active')
    await message.answer('Ты больше не забанен.')


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='Мой профиль')
async def profile(message: Message):
    try:
        print('profile')
        await message.delete()
        user = await commands.select_user(message.from_user.id)
        print(user)
        if user is not None:
            pass
        print(os.getcwd())
        photo_bytes = types.InputFile(path_or_bytesio=f'{user.avatar}')
        await dp.bot.send_photo(
            message.from_user.id,
            photo=photo_bytes,
            caption=
            f'Имя: <b>{user.first_name}</b>\n'
            f'\n'
            f'Фамилия: <b>{user.last_name}</b>\n'
            f'\n'
            f'Город: <b>{user.address}</b>\n'
            f'\n'
            f'Организация: <b>{user.corporation}</b>\n'
            f'\n'
            f'О себе: <b>{user.about}</b>\n'
        )
        # await message.answer(
        #
        #     f'Имя: <b>{user.first_name}</b>\n'
        #     f'\n'
        #     f'Фамилия: <b>{user.last_name}</b>\n'
        #     f'\n'
        #     f'Город: <b>{user.address}</b>\n'
        #     f'\n'
        #     f'Организация: <b>{user.corporation}</b>\n'
        #     f'\n'
        #     f'О себе: <b>{user.about}</b>\n'
        # ),
    except Exception as ex:
        await message.answer('Сначала пройдите регистрацию')
        await message.answer('Указать информацию', reply_markup=kb_register)
        print(ex)


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='Редактировать')
async def profile_edit(message: Message):
    try:
        user = await commands.select_user(message.from_user.id)
        if user is not None:
            await message.answer(
                text="Что будем редактировать",
                reply_markup=ikb_profile_edit,
            )
        else:
            await message.delete()
            await message.answer('Сначала пройдите регистрацию')
            await message.answer('Указать информацию', reply_markup=kb_register)

    except Exception as ex:
        print(ex)


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='Нетворкинг')
async def networking(message: Message):
    try:
        user = await commands.select_user(message.from_user.id)
        if user is not None:
            await message.answer(
                text="Список всех участников",
                reply_markup=ikb_mem_networking,
            )
        else:
            await message.delete()
            await message.answer('Сначала пройдите регистрацию')
            await message.answer('Указать информацию', reply_markup=kb_register)
    except Exception as ex:
        print(ex)


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='Прошедшие мероприятия')
async def events_last(message: Message):
    try:
        await message.delete()
        user = await commands.select_user(message.from_user.id)
        if user is not None:
            await message.answer(text="Список прошедших мероприятии", reply_markup=ikb_last)
        else:
            await message.answer('Сначала пройдите регистрацию')
            await message.answer('Указать информацию', reply_markup=kb_register)
    except Exception as ex:
        print(ex)


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='Будущие мероприятия')
async def events_future(message: Message):
    try:
        await message.delete()
        user = await commands.select_user(message.from_user.id)
        if user is not None:
            await message.answer(text="Список будущих мероприятии", reply_markup=ikb_future)
        else:
            await message.answer('Сначала пройдите регистрацию')
            await message.answer('Указать информацию', reply_markup=kb_register)
    except Exception as ex:
        print(ex)


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='back')
async def get_back(message: types.Message):
    try:
        await message.delete()
        await message.answer(text='Меню ниже', reply_markup=await kb_menus(message.from_user.id))
    except Exception as ex:
        print(ex)


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='Отменить')
async def get_cancel(message: types.Message):
    try:
        await message.delete()
        await message.answer(text='Меню ниже', reply_markup=await kb_menus(message.from_user.id))
    except Exception as ex:
        print(ex)


@rate_limit(limit=3)
@dp.message_handler(regexp='^even_[a-z0-9]+')
async def get_event(message: types.Message):
    await message.delete()
    try:
        print('get_event')
        evens = await events.select_all_events()
        for even in evens:
           if even.deleted_at is None:
               print(even.id)
               strId = str(even.id)
               result_id: str = hashlib.md5(strId.encode()).hexdigest()
               st = str(os.getenv('token')) + str(even.id)
               evets_id: str = hashlib.md5(st.encode()).hexdigest()

               owd = os.getcwd()
               photo_bytes = types.InputFile(path_or_bytesio=f'{even.cover}')
               if 'even_' + result_id == message.text:
                   await dp.bot.send_photo(message.from_user.id, photo=photo_bytes,
                                           caption=
                                           f'Название: <b>{even.name}</b>\n\n'
                                           f'Описание: \n<b>{even.desc[:200]}</b>\n\n'
                                           f'Программа: \n<b>{even.program[:200]}</b>\n\n'
                                           f'Дата: \n<b>{even.date}</b>\n',
                                           reply_markup=types.InlineKeyboardMarkup(
                                               row_width=2,
                                               inline_keyboard=[
                                                   [
                                                       types.InlineKeyboardButton(
                                                           text='Нетворкинг',
                                                           switch_inline_query_current_chat=f'Участники_{evets_id}_{strId}',
                                                           # callback_data=f'get_networking_{even.id}'
                                                       ),
                                                       types.InlineKeyboardButton(
                                                           text='Принять участие',
                                                           callback_data=f'submit_{even.id}'),
                                                       types.InlineKeyboardButton(
                                                           text='Получить файлы',
                                                           callback_data=f'get_file_{even.id}')
                                                   ],
                                               ]
                                           ))
    except Exception as ex:
        print(ex)


@rate_limit(limit=3)
@dp.message_handler(regexp='^last_[a-z0-9]+')
async def get_last_event(message: types.Message):
    await message.delete()
    try:
        print('get_last_event')
        evens = await events.select_all_events()
        for even in evens:
            strId = str(even.id)
            result_id: str = hashlib.md5(strId.encode()).hexdigest()
            st = str(os.getenv('token')) + str(even.id)
            evets_id: str = hashlib.md5(st.encode()).hexdigest()
            photo_bytes = types.InputFile(path_or_bytesio=even.cover)
            if 'last_' + result_id == message.text:
                await dp.bot.send_photo(message.from_user.id, photo=photo_bytes,
                                        caption=
                                        f'Название: <b>{even.name}</b>\n\n'
                                        f'Описание: \n<b>{even.desc[:200]}</b>\n\n'
                                        f'Программа: \n<b>{even.program[:200]}</b>\n\n'
                                        f'Дата: \n<b>{even.date}</b>\n',
                                        reply_markup=types.InlineKeyboardMarkup(
                                            row_width=2,
                                            inline_keyboard=[
                                                [
                                                    types.InlineKeyboardButton(
                                                        text='Нетворкинг',
                                                        switch_inline_query_current_chat=f'Участники_{evets_id}_{strId}',
                                                        # callback_data=f'get_networking_{even.id}'
                                                    ),
                                                    types.InlineKeyboardButton(
                                                        text='Получить файлы',
                                                        callback_data=f'get_file_{even.id}')
                                                ],
                                            ]
                                        ))
    except Exception as ex:
        print(ex)


@dp.message_handler(regexp='^members_[a-z0-9]+_eve_[0-9]')
async def members_(message: types.Message):
    try:
        print('members_')
        await message.delete()
        user_pass = message.text.split('_')[1]
        users = await select_all_users()
        passwo = str(os.getenv('token'))

        for user in users:
            str_check = str(user.id) + passwo
            check: str = hashlib.md5(str_check.encode()).hexdigest()
            if check == user_pass:
                event_pass = message.text.split('_')[3]
                photo_bytes = types.InputFile(path_or_bytesio=f'{user.avatar}')
                ids = user.tg_user_id
                froms = message.from_user.id
                await dp.bot.send_photo(
                    message.from_user.id,
                    photo=photo_bytes,
                    caption=f'Имя: <b>{user.first_name}</b>\n'
                            f'\n'
                            f'Фамилия: <b>{user.last_name}</b>\n'
                            f'\n'
                            f'Город: <b>{user.address}</b>\n'
                            f'\n'
                            f'Организация: <b>{user.corporation}</b>\n'
                            f'\n'
                            f'О себе: <b>{user.about}</b>\n',
                    reply_markup=types.InlineKeyboardMarkup(
                        row_width=2,
                        inline_keyboard=[
                            [
                                types.InlineKeyboardButton(
                                    text='Написать',
                                    callback_data=f'req_{ids}_from_{froms}_event_{event_pass} '
                                ),

                            ],
                        ]
                    ))

    except AttributeError as ex:

        print(ex)


@dp.message_handler(regexp='^one_members_[0-9]')
async def members_one(message: types.Message):
    try:
        print('members_one')
        await message.delete()
        user_id = message.text.split('_')[2]
        user = await select_id(int(user_id))
        photo_bytes = types.InputFile(path_or_bytesio=f'{user.avatar}')
        ids = user.tg_user_id

        froms = message.from_user.id
        await dp.bot.send_photo(
            message.from_user.id,
            photo=photo_bytes,
            caption=f'Имя: <b>{user.first_name}</b>\n'
                    f'\n'
                    f'Фамилия: <b>{user.last_name}</b>\n'
                    f'\n'
                    f'Город: <b>{user.address}</b>\n'
                    f'\n'
                    f'Организация: <b>{user.corporation}</b>\n'
                    f'\n'
                    f'О себе: <b>{user.about}</b>\n',
            reply_markup=types.InlineKeyboardMarkup(
                row_width=2,
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text='Написать',
                            callback_data=f'req_{ids}_from_{froms} '
                        ),

                    ],
                ]
            ))



    except AttributeError as ex:

        print(ex)


@rate_limit(limit=3)
@dp.message_handler(regexp='^my_even_[0-9]+')
async def get_my_event(message: types.Message):
    print('get_my_event')
    event_id = message.text.split('_')[2]
    await message.delete()
    try:
        even = await select_my_events(int(event_id))
        photo_bytes = types.InputFile(path_or_bytesio=f'{even.cover}')
        await dp.bot.send_photo(message.from_user.id, photo=photo_bytes,
                                caption=
                                f'Название: <b>{even.name}</b>\n'
                                f'Описание: <b>{even.desc}</b>\n'
                                f'Программа: <b>{even.program}</b>\n'
                                f'Дата: <b>{even.date}</b>\n',
                                reply_markup=types.InlineKeyboardMarkup(
                                    row_width=2,
                                    inline_keyboard=[
                                        [
                                            types.InlineKeyboardButton(
                                                text='Нетворкинг',
                                                switch_inline_query_current_chat=f'Участники_{str(event_id)}_{str(even.id)}',
                                                # callback_data=f'get_networking_{even.id}'
                                            ),
                                            types.InlineKeyboardButton(
                                                text='Принять участие',
                                                callback_data=f'submit_{str(even.id)}'),
                                            types.InlineKeyboardButton(
                                                text='Получить файлы',
                                                callback_data=f'get_file_{str(even.id)}'),
                                        ],

                                    ]
                                )
                                )
        await dp.bot.send_message(message.from_user.id, text='Меню ниже',
                                  reply_markup=types.ReplyKeyboardMarkup(
                                      keyboard=[
                                          [
                                              KeyboardButton(text='Мои Мероприятия'),
                                          ],
                                          [
                                              KeyboardButton(text='Удалить'),
                                          ],

                                      ],
                                      resize_keyboard=True,
                                      one_time_keyboard=True
                                  ))

    except Exception as ex:
        print(ex)


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='Мои Мероприятия')
async def events_mod(message: Message):
    try:
        await message.delete()
        user = await commands.select_user(message.from_user.id)
        if user is not None:
            await message.answer(text="Список моих мероприятии", reply_markup=ikb_my)
        else:
            await message.answer('Сначала пройдите регистрацию')
            await message.answer('Указать информацию', reply_markup=kb_register)
    except Exception as ex:
        print(ex)


@rate_limit(limit=3)
@dp.message_handler(regexp='^mod_even_[0-9]+')
async def mod_even_(message: types.Message):
    await message.delete()
    try:
        print('mod_even_')

        even = await events.select_event(int(message.text.split('_')[2]))

        photo_bytes = types.InputFile(path_or_bytesio=f'{even.cover}', )
        await dp.bot.send_photo(message.from_user.id, photo=photo_bytes,
                                caption=
                                f'Название: <b>{even.name}</b>\n'
                                f'Описание: <b>{even.desc}</b>\n'
                                f'Программа: <b>{even.program}</b>\n'
                                f'Дата: <b>{even.date}</b>\n',
                                reply_markup=types.InlineKeyboardMarkup(
                                    row_width=2,
                                    inline_keyboard=[
                                        [
                                            types.InlineKeyboardButton(
                                                text='Название',
                                                callback_data=f'edit_my_event_name_{even.id}'
                                            ),
                                            types.InlineKeyboardButton(
                                                text='Описание',
                                                callback_data=f'edit_my_event_desc_{even.id}'),
                                        ],
                                        [
                                            types.InlineKeyboardButton(
                                                text='Программа',
                                                callback_data=f'edit_my_event_program_{even.id}'),
                                            types.InlineKeyboardButton(
                                                text='Дата',
                                                callback_data=f'edit_my_event_date_{even.id}')
                                        ],
                                        [
                                            types.InlineKeyboardButton(
                                                text='Обложка',
                                                callback_data=f'edit_my_event_cover_{even.id}'),
                                        ],
                                    ]))


    except Exception as ex:
        print(ex)

# callback_data=f'edit_my_{str(even.id)}'),
# callback_data = f'del_my_{str(even.id)}'),

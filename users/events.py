import hashlib
import os
import time
from datetime import datetime

from aiogram import types

from keybords.default import kb_menus, kb_register
from keybords.inline import ikb_my_event_edit
from loader import dp, bot
from utils.db_api import event_commands as commands
from utils.db_api import quick_commands as users
from utils.db_api.event_commands import select_all_events, count_events, select_event
from utils.db_api.events_files import select_event_files
from utils.db_api.events_members_commands import add_event_member, select_all_members
from utils.db_api.files_command import select_file
from utils.db_api.members_commands import select_members, add_member, select_user_id
from utils.db_api.moderator_commands import select_all_my_events
from utils.db_api.quick_commands import select_user, select_all_users
from utils.db_api.members_commands import select_all_members as alm
from utils.db_api.quick_commands import select_id
from utils.db_api.requests_commands import add_request, check_exist_networking


@dp.inline_handler(lambda query: query.query == 'Нетворкинг')
async def get_networking(inline_query: types.InlineQuery):
    try:
        print('get_networking')
        mem = []
        all_members = await select_all_users()

        for user in all_members:

            if user.id is not None:
                input_content = types.InputTextMessageContent(f'one_members_{user.id}', parse_mode='html')
                mem.append(
                    types.InlineQueryResultArticle(
                        id=f'{user.id}',
                        title=f'{user.first_name}',
                        # url=f'{os.getenv("BASE_URL")}/{user.avatar}',
                        hide_url=True,
                        thumb_url=f'{os.getenv("BASE_URL")}/{user.avatar}',
                        input_message_content=input_content,
                        description=f'Что ищите: {user.what[:10]} \nГород: {user.address} ',
                        thumb_width=70,
                        thumb_height=70,
                    ),
                )
            else:
                pass

        mem.append(
            types.InlineQueryResultArticle(
                id=f'123123',
                title='◀️ Назад',
                # url='https://source.unsplash.com/featured/300x202',
                hide_url=True,
                thumb_url='https://cdn-icons-png.flaticon.com/512/122/122641.png',
                input_message_content=types.InputTextMessageContent('back'),
                description='Вернутся в меню',
                thumb_width=100,
                thumb_height=70,
            ),

        )
        await dp.bot.answer_inline_query(inline_query.id, results=mem, cache_time=10, switch_pm_text='', )
    except Exception as ex:
        print(ex)


# @dp.callback_query_handler(lambda c: c.data and c.data.startswith('get_last_events_'))
# async def get_events(callback_query: types.CallbackQuery):
#     datas = callback_query.data
#     print(datas)
#     code = [int(s) for s in datas.split('_') if s.isdigit()]
#     try:
#         event = await commands.select_event(code[0])
#         await bot.send_message(callback_query.from_user.id, (
#             f'{event.name}\n'
#             f'\n'
#             f'{event.desc}\n'
#             f'\n'
#             f'{event.program}\n'
#             f'\n'
#             f'{event.speaker_id}\n'
#             f'\n'
#             f'{event.created_at}\n'
#         ))
#
#     except AttributeError as ex:
#         await bot.send_message(callback_query.from_user.id, text='Информация отсуствует в базе')
#
#
# @dp.callback_query_handler(lambda c: c.data and c.data.startswith('events_'))
# async def get_all_events(callback_query: types.CallbackQuery):
#     datas = callback_query.data
#     print(datas)
#     try:
#
#         event = await commands.select_all_events_as_button()
#         print(event)
#     except AttributeError as ex:
#         await bot.send_message(callback_query.from_user.id, text='Информация отсуствует в базе')
#


@dp.inline_handler(lambda query: query.query == 'Мои')
async def my_event_edit(inline_query: types.InlineQuery):
    try:
        user = await users.select_user(inline_query.from_user.id)
        if user is not None:
            await dp.bot.send_message(
                inline_query.from_user.id,
                text="Выберете мероприятие для редактировать",
            )
            events = await select_all_my_events(user.id)
            print(events)
            my_items = []
            for keys in events:
                find_event = await select_event(keys.events_id)
                print(find_event)
                if find_event.deleted_at is None:
                    input_content = types.InputTextMessageContent('mod_even_' + str(find_event.id), parse_mode='html')

                    my_items.append(
                        types.InlineQueryResultArticle(
                            id=f'{find_event.id}',
                            title=f'{find_event.name}',
                            # url=f'{os.getenv("BASE_URL")}/storage/{find_event.cover}',
                            hide_url=True,
                            thumb_url=f'{os.getenv("BASE_URL")}/storage/{find_event.cover}',
                            input_message_content=input_content,
                            description=f'{find_event.date}\n{find_event.desc}',
                            thumb_width=100,
                            thumb_height=70,
                            reply_markup=ikb_my_event_edit
                        ),

                    )

            my_items.append(
                types.InlineQueryResultArticle(
                    id=f'123123',
                    title='◀️ Назад',
                    # url='https://source.unsplash.com/featured/300x202',
                    hide_url=True,
                    thumb_url='https://cdn-icons-png.flaticon.com/512/122/122641.png',
                    input_message_content=types.InputTextMessageContent('back'),
                    description='Вернутся в меню',
                    thumb_width=100,
                    thumb_height=70,
                ),

            )

            await dp.bot.answer_inline_query(inline_query.id, results=my_items, cache_time=10, switch_pm_text='', )
        else:
            await dp.bot.message.delete()
            await dp.bot.message.answer('Сначала пройдите регистрацию')
            await dp.bot.message.answer('Указать информацию', reply_markup=kb_register)

    except Exception as ex:
        print(ex)


@dp.inline_handler(lambda query: query.query == 'Прошедшие')
async def get_last_events(inline_query: types.InlineQuery):
    try:
        print('get_last_events')
        datetimenow = datetime.utcnow().strftime('%d-%m-%Y %H-%M-%S')
        events = await commands.select_all_events()
        text = inline_query.query or 'echo'
        items = []
        for keys in events:
            now = time.strptime(datetimenow, '%d-%m-%Y %H-%M-%S')
            last = time.strptime(keys.date, '%d-%m-%Y %H-%M-%S')
            if now > last and keys.deleted_at is None:
                strId = str(keys.id)
                result_id: str = hashlib.md5(strId.encode()).hexdigest()
                input_content = types.InputTextMessageContent('last_' + result_id, parse_mode='html')
                items.append(
                    types.InlineQueryResultArticle(
                        id=f'{keys.id}',
                        title=f'{keys.name}',
                        # url=f'{os.getenv("BASE_URL")}/{keys.cover}',
                        hide_url=True,
                        thumb_url=f'{os.getenv("BASE_URL")}/{keys.cover}',
                        input_message_content=input_content,
                        description=f'{keys.date}\n{keys.desc[:150]}',
                        thumb_width=100,
                        thumb_height=70,
                    ),

                )

        items.append(
            types.InlineQueryResultArticle(
                id=f'123123',
                title='◀️ Назад',
                # url='https://source.unsplash.com/featured/300x202',
                hide_url=True,
                thumb_url='https://cdn-icons-png.flaticon.com/512/122/122641.png',
                input_message_content=types.InputTextMessageContent('back'),
                description='Вернутся в меню',
                thumb_width=100,
                thumb_height=70,
            ),
        )
        await bot.answer_inline_query(inline_query.id, results=items, cache_time=10, switch_pm_text='', )
    except Exception as ex:
        print(ex)


@dp.inline_handler(lambda query: query.query == 'Будущие')
async def get_future_events(inline_query: types.InlineQuery):
    try:
        print('get_future_events')
        datetimenow = datetime.utcnow().strftime('%d-%m-%Y %H-%M-%S')
        events = await commands.select_all_events()

        items = []
        for keys in events:
            print(keys.deleted_at)
            now = time.strptime(datetimenow, '%d-%m-%Y %H-%M-%S')
            last = time.strptime(keys.date, '%d-%m-%Y %H-%M-%S')
            if now < last and keys.deleted_at is None:
                strId = str(keys.id)
                result_id: str = hashlib.md5(strId.encode()).hexdigest()
                input_content = types.InputTextMessageContent('even_' + result_id, parse_mode='html')

                items.append(
                    types.InlineQueryResultArticle(
                        id=f'{keys.id}',
                        title=f'{keys.name}',
                        # url=f'{os.getenv("BASE_URL")}/storage/{keys.cover}',
                        hide_url=True,
                        thumb_url=f'{os.getenv("BASE_URL")}/storage/{keys.cover}',
                        input_message_content=input_content,
                        description=f'{keys.date}\n{keys.desc}',
                        thumb_width=100,
                        thumb_height=70,
                    ),

                )

        items.append(
            types.InlineQueryResultArticle(
                id=f'123123',
                title='◀️ Назад',
                # url='https://source.unsplash.com/featured/300x202',
                hide_url=True,
                thumb_url='https://cdn-icons-png.flaticon.com/512/122/122641.png',
                input_message_content=types.InputTextMessageContent('back'),
                description='Вернутся в меню',
                thumb_width=100,
                thumb_height=70,
            ),

        )

        await bot.answer_inline_query(inline_query.id, results=items, cache_time=10, switch_pm_text='', )
    except Exception as ex:
        print(ex)


@dp.callback_query_handler(regexp='^submit_[0-9]+')
async def submit_(callback_query: types.CallbackQuery):
    try:
        print('submit_')
        event_id = callback_query.data.split('_')[1]

        tg_id = callback_query.from_user.id
        user = await users.select_user_id(tg_id)
        await bot.send_message(
            callback_query.from_user.id,
            'Принять участие',
            reply_markup=types.InlineKeyboardMarkup(
                row_width=2,
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text='Присутствовать очно',
                            callback_data=f'seteve_1_{event_id}_{user.id}'
                        ),
                        types.InlineKeyboardButton(
                            text='Присутствовать дистанционно',
                            callback_data=f'seteve_0_{event_id}_{user.id}'),
                    ],
                ]))
        # user.id
    except Exception as ex:
        print(ex)


@dp.inline_handler(regexp='Участники_[a-z0-9]+')
async def get_networking_(inline_query: types.InlineQuery):
    try:
        print('get_networking_')
        event = inline_query.query.split('_')
        passw = event[2]
        events = await select_event(int(passw))
        passwo = str(os.getenv('token'))
        mem = []

        all_members = await select_all_members(events.id)
        for member in all_members:
            members_id = await select_members(member.members_id)
            user = await select_id(members_id.user_id)
            if user.id is not None:
                check = str(user.id) + passwo
                mem_pass: str = hashlib.md5(check.encode()).hexdigest()
                input_content = types.InputTextMessageContent(f'members_{mem_pass}_eve_{passw}', parse_mode='html')
                mem.append(
                    types.InlineQueryResultArticle(
                        id=f'{user.id}',
                        title=f'{user.first_name}',
                        # url=f'{os.getenv("BASE_URL")}/{user.avatar}',
                        hide_url=True,
                        thumb_url=f'{os.getenv("BASE_URL")}/{user.avatar}',
                        input_message_content=input_content,
                        description=f'О себе: {user.what} \nГород: {user.address} ',
                        thumb_width=70,
                        thumb_height=70,
                    ),
                )
            else:
                pass
        mem.append(
            types.InlineQueryResultArticle(
                id=f'123123',
                title='◀️ Назад',
                # url='https://source.unsplash.com/featured/300x202',
                hide_url=True,
                thumb_url='https://cdn-icons-png.flaticon.com/512/122/122641.png',
                input_message_content=types.InputTextMessageContent('back'),
                description='Вернутся в меню',
                thumb_width=100,
                thumb_height=70,
            ),

        )
        await bot.answer_inline_query(inline_query.id, results=mem, cache_time=10, switch_pm_text='', )
    except Exception as ex:
        print(ex)


# @dp.callback_query_handler(regexp='^get_networking_[0-9]+')
# async def networking_(callback_query: types.CallbackQuery):
#     try:
#         network_id = callback_query.data.split('_')[2]
#         networks = await select_all_members(int(network_id))
#         print(len(networks))
#         for network in networks:
#             member = await select_members(network.members_id)
#             user_info = await users.select_id(member.user_id)
#
#             await bot.send_message(
#                 callback_query.from_user.id,
#                 f'Имя: <b>{user_info.first_name}</b>\n'
#                 f'\n'
#                 f'Фамилия: <b>{user_info.last_name}</b>\n'
#                 f'\n'
#                 f'Город: <b>{user_info.address}</b>\n'
#                 f'\n'
#                 f'Организация: <b>{user_info.corporation}</b>\n'
#                 f'\n'
#                 f'О себе: <b>{user_info.about}</b>\n'
#                 ,
#                 reply_markup=types.InlineKeyboardMarkup(
#                     row_width=2,
#                     inline_keyboard=[
#                         [
#                             types.InlineKeyboardButton(
#                                 text='Написать',
#                                 callback_data=f'send_req_{user_info.tg_user_id}_from_{callback_query.from_user.id}'
#                             ),
#                         ],
#                     ]
#                 ))
#
#         # tg_id = callback_query.from_user.id
#         # user = await users.select_user_id(tg_id)
#
#     except Exception as ex:
#         print(ex)


@dp.callback_query_handler(regexp='^req_[0-9]+_from_[0-9]+')
async def send_req_one_events(callback_query: types.CallbackQuery):
    try:
        print('send_req_one_events')
        lists = callback_query.data.split('_')
        req_from = callback_query.data.split('_')[3]
        req_to = callback_query.data.split('_')[1]
        event_id = None
        if 'event' in lists:
            event_id = callback_query.data.split('_')[5]
            val = f'_event_{event_id}'
        else:
            val = ''

        user_req_to = await select_user(req_to)
        user_req_from = await select_user(req_from.strip())

        result_check = await check_exist_networking(user_req_from.id, user_req_to.id)
        print(result_check)
        if result_check is None:
            await add_request(user_req_from.id, 1, 0, user_req_to.id)
            invite_msg = f'Привет! Тебе поступило приглашение на общение от {user_req_from.first_name}'
            sender_msg = f'Приглашение успешно отправлено участнику: {user_req_to.first_name}'
            await dp.bot.send_message(
                chat_id=req_from.strip(),
                text=sender_msg,
                reply_markup=await kb_menus(req_from.strip())
            )
            await bot.send_message(
                chat_id=req_to,
                text=invite_msg,
                reply_markup=types.InlineKeyboardMarkup(
                    row_width=2,
                    inline_keyboard=[
                        [
                            types.InlineKeyboardButton(
                                text='Принять приглашение',
                                callback_data=f'send_response_1_from_{req_from.strip()}_to_{req_to}{val}'
                            ),
                            types.InlineKeyboardButton(
                                text='Отказаться',
                                callback_data=f'send_response_0_from_{req_from.strip()}_to_{req_to}{val}'
                            ),
                        ],
                    ]
                ))
        else:
            sender_msg = f'{user_req_to.first_name} принял Ваше приглашение на общение!'
            await dp.bot.send_message(
                chat_id=req_from.strip(),
                text=f'{sender_msg} @{user_req_to.tg_username}',
                reply_markup=await kb_menus(req_from.strip())
            )








    except Exception as ex:
        print(ex)


#
#
@dp.callback_query_handler(regexp='send_response_[0-9]_from_[0-9]+_to_[0-9]+')
async def send_response_events(callback_query: types.CallbackQuery):
    try:
        print('send_response_events')
        event_id = None
        lists = callback_query.data.split('_')
        if 'event' in lists:
            event_id = callback_query.data.split('_')[8]
            val = f'_event_{event_id}'
        else:
            val = ''

        answer = callback_query.data.split('_')[2]
        res_from = callback_query.data.split('_')[4].strip()
        res_to = callback_query.data.split('_')[6].strip()

        user_from = await users.select_user_id(res_from)
        user_to = await users.select_user_id(res_to)
        if answer == '1':
            text = f'Вы одобрили заявку на общения для {user_from.first_name} @{user_from.tg_username}! Приятного общения'
            send_msg = f'{user_to.first_name} принял Ваше приглашение на общение!'
            await bot.send_message(
                callback_query.from_user.id,
                text,
            )
            await bot.send_message(
                res_from,
                send_msg + f' @{user_to.tg_username}',

            )
        elif answer == '0':
            text = f'Вы не приняли приглашение от {user_from.first_name}.'
            send_msg = f'{user_to.first_name} не приняла Ваше приглашение. Вернуться к списку участников?'
            await bot.send_message(
                res_to,
                text,
                reply_markup=types.InlineKeyboardMarkup(
                    row_width=1,
                    inline_keyboard=[
                        [
                            types.InlineKeyboardButton(
                                text='Вернуться к главному меню?',
                                callback_data='back'
                            ),

                        ],
                    ]
                )
            )
            st = str(os.getenv('token')) + str(event_id)
            evets_id: str = hashlib.md5(st.encode()).hexdigest()
            await bot.send_message(
                res_to,
                send_msg,
                reply_markup=types.InlineKeyboardMarkup(
                    row_width=2,
                    inline_keyboard=[
                        [
                            types.InlineKeyboardButton(
                                text='Да',
                                switch_inline_query_current_chat=f'Участники_{evets_id}_{event_id}',
                            ),
                            types.InlineKeyboardButton(
                                text='Нет',
                                callback_data=f'back'
                            ),
                        ],
                    ]
                )
            )

    except AttributeError as ex:

        print(ex)


@dp.callback_query_handler(regexp='^seteve_[0-9]+_[a-z0-9]_[0-9]')
async def seteve_(callback_query: types.CallbackQuery):
    try:
        print(callback_query.data.split('_'))
        in_person, event_id, user_id = callback_query.data.split('_')[1:]
        event = await select_event(int(event_id))
        member = await select_user_id(int(user_id))

        result = await add_event_member(int(event_id), int(member.id), int(in_person))
        print(result)
        if result is not None:
            await bot.send_message(
                callback_query.from_user.id,
                f'Вы успешно добавлены в список участников мероприятия {event.name}',
                # reply_markup=kb_networking
            )

    except AttributeError as ex:
        print(ex)


@dp.callback_query_handler(regexp='^get_file_[0-9]+')
async def get_file_(callback_query: types.CallbackQuery):
    try:
        event_id = callback_query.data.split('_')[2:][0]
        files = await select_event_files(int(event_id))
        files_path = []
        os.getcwd()
        owd = os.getcwd()
        media = types.MediaGroup()
        for file in files:
            fil = await select_file(file.files_id)
            # if fil is not None:
            photo_bytes = types.InputFile(path_or_bytesio=f'{fil.path}')
            media.attach_document(document=photo_bytes)

            # await dp.bot.send_message(callback_query.from_user.id, photo=photo_bytes)
        await callback_query.message.answer_media_group(media=media)
    except AttributeError as ex:

        print(ex)


@dp.callback_query_handler(text='back')
async def get_back(calback_query: types.CallbackQuery):
    try:
        user_id = calback_query.from_user.id
        await calback_query.message.delete()
        await calback_query.message.answer(text='Меню ниже', reply_markup=await kb_menus(user_id))
    except Exception as ex:
        print(ex)

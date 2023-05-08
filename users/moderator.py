import hashlib
import os
import time
from datetime import datetime
import socket
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import callback_query

from loader import dp
from states import edit_sevents
from utils.db_api import event_commands, moderator_commands
from utils.db_api.event_commands import select_event, update_event_name
from utils.db_api.moderator_commands import select_all_my_events, update_my_event_name
from utils.db_api.quick_commands import select_user
from utils.misc import rate_limit


@dp.inline_handler(lambda query: query.query == 'Мои')
async def my_all_events(inline_query: types.InlineQuery):
    try:
        users = inline_query.from_user.id

        user = await select_user(users)
        # print(user )
        events = await select_all_my_events(user.id)
        #

        owd = os.getcwd()
        items = []
        for keys in events:
            strId = str(keys.id)
            # result_id: str = hashlib.md5(strId.encode()).hexdigest()
            input_content = types.InputTextMessageContent('my_even_' + strId, parse_mode='html')

            items.append(
                types.InlineQueryResultArticle(
                    id=f'{keys.id}',
                    title=f'{keys.name}',
                    url=f'https://assets.fireside.fm/file/fireside-images/podcasts/images/b/bc7f1faf-8aad-4135-bb12-83a8af679756/cover_small.jpg',
                    # url=f'http://94.228.120.114/storage/{keys.cover}',
                    hide_url=True,
                    # thumb_url=f'{keys.cover}',
                    thumb_url=f'https://assets.fireside.fm/file/fireside-images/podcasts/images/b/bc7f1faf-8aad-4135-bb12-83a8af679756/cover_small.jpg',
                    # thumb_url=f'http://94.228.120.114/storage/{keys.cover}',
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

        await dp.bot.answer_inline_query(inline_query.id, results=items, cache_time=10, switch_pm_text='', )
    except Exception as ex:
        print(ex)


@dp.callback_query_handler(regexp='^del_my_[0-9]+')
async def del_my_(callback_query: types.CallbackQuery):
    try:
        print(callback_query.data)
    except Exception as ex:
        print(ex)


@rate_limit(limit=3)
@dp.callback_query_handler(regexp='^edit_my_event_[a-z]+_[0-9]+')
async def edit_my_event_name_(callback_query: types.CallbackQuery):
    try:
        print(callback_query.data.split('_'))
        what = callback_query.data.split('_')[3]
        event_id = callback_query.data.split('_')[4]
        event = await select_event(int(event_id))



        # elif what == 'desc':
        #     await dp.bot.send_message(callback_query.from_user.id, text='Напишите описание мероприятие')
        # elif what == 'program':
        #     await dp.bot.send_message(callback_query.from_user.id, text='Напишите программу мероприятие')
        # elif what == 'date':
        #     await dp.bot.send_message(callback_query.from_user.id, text='Напишите дату мероприятие')
        # elif what == 'cover':
        #     await dp.bot.send_message(callback_query.from_user.id, text='Пришлите обложку мероприятие')

    except Exception as ex:
        print(ex)


@dp.callback_query_handler(state=edit_sevents.id)
async def id_(callback: types.CallbackQuery, state: FSMContext):
    try:
        await dp.bot.send_message(callback.from_user.id, text='Напишите название мероприятие')
        await edit_sevents.name.set()
    except Exception:
        await callback.answer(f'Чтото не так')


@dp.message_handler(state=edit_sevents.name)
async def about_(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        await state.update_data(name=answer)

        await update_event_name(name=answer)
        await state.finish()
    except Exception:
        await message.answer(f'Чтото не так')


# @dp.callback_query_handler(regexp='^edit_desc_[0-9]+')
# async def edit_my_event_desc(callback_query: types.CallbackQuery):
#     try:
#         await dp.bot.send_message(callback_query.from_user.id, 'Напишите описание мероприятие')
#
#         await edit_sevents.desc.set()
#     except Exception as ex:
#         print(ex)
#
#
# @dp.callback_query_handler(regexp='^edit_date_[0-9]+')
# async def edit_my_event_date(callback_query: types.CallbackQuery):
#     try:
#         await dp.bot.send_message(callback_query.from_user.id, 'Напишите дату мероприятие')
#
#         await edit_sevents.date.set()
#     except Exception as ex:
#         print(ex)
#
#
# @dp.callback_query_handler(regexp='^edit_cover_[0-9]+')
# async def edit_my_event_cover(callback_query: types.CallbackQuery):
#     try:
#         await dp.bot.send_message(callback_query.from_user.id, 'Напишите дату мероприятие')
#
#         await edit_sevents.cover.set()
#     except Exception as ex:
#         print(ex)
#
#
# @dp.callback_query_handler(regexp='^edit_program_[0-9]+')
# async def edit_my_event_program(callback_query: types.CallbackQuery):
#     try:
#         await dp.bot.send_message(callback_query.from_user.id, 'Напишите программу мероприятие')
#
#         await edit_sevents.program.set()
#     except Exception as ex:
#         print(ex)

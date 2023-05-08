from aiogram import types
from aiogram.dispatcher.filters import Command

from handlers.users.add_events import add_events_
from keybords.default import kb_menus
from keybords.default.keyboard_menu import kb_menus
from keybords.inline import ikb_moderator
from loader import dp
from utils.db_api.moderator_commands import add_to_moderator
from utils.db_api.quick_commands import select_user_id


@dp.message_handler(Command("menu"))
async def menu(message: types.Message):
    await message.delete()
    try:

        await message.answer('Меню ниже', reply_markup=await kb_menus(message.from_user.id))
    except Exception as ex:
        print(ex)


@dp.message_handler(text="Стать модератором")
async def menu(message: types.Message):
    await message.delete()
    user_tg_id = message.from_user.id
    user_id = await select_user_id(user_tg_id)
    await add_to_moderator(user_id.id)
    await message.answer('Ваш запрос отправлен нашим администраторам на проверку - ожидайте кода модератора',
                         reply_markup=await kb_menus(message.from_user.id))


@dp.message_handler(text='Создать мероприятие')
async def _events_(message: types.Message):
    await message.delete()
    await add_events_()


@dp.message_handler(text='Мои мероприятия')
async def _events_(message: types.Message):
    await message.delete()
    await message.answer('Открыть', reply_markup=ikb_moderator.ikb_my)

# @dp.message_handler(Command("Мой профиль"))
# async def menu(message: types.Message):
#     await message.delete()
#     await message.answer('Выбери меню ниже', reply_markup=ikb_profile)

from aiogram import types
from loader import dp


@dp.message_handler(text='profile')
async def buttons_test(message: types.Message):
    print(message.from_user)
    await message.answer(f'Привет {message.from_user.full_name}!\n'
                         f'Ты выбрал: {message.text}')


# @dp.message_handler(text='Указать информацию')
# async def buttons_test(message: types.Message):
#     await message.answer(f'/register')


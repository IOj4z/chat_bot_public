from aiogram import types
from aiogram.types import CallbackQuery

from keybords.default import kb_register

from keybords.inline.inline_kb_file import ikb_file
from keybords.inline.inline_kb_profile import ikb_profile_edit
from loader import dp


@dp.message_handler(text='Мой профиль')
async def show_inline_profile(call: CallbackQuery):
    await call.message.answer('Кнопки заменены', reply_markup=ikb_profile_edit)


@dp.callback_query_handler(text='Указать информацию')
async def show_message(call: CallbackQuery):
    await call.message.answer('Так давайте начнем', reply_markup=kb_register)


@dp.callback_query_handler(text='Получить файлы')
async def show_message(message: types.Message):
    await message.answer('Получить файлы', reply_markup=ikb_file)


@dp.callback_query_handler(text='alert')
async def show_message(call: CallbackQuery):
    await call.answer('Кнопки заменены', show_alert=True)

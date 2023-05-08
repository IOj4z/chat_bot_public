import io
import logging
import os
import shutil
from PIL import Image, ImageFilter
from datetime import datetime
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from filters import IsPrivate
from keybords.default import kb_menus
from keybords.default.keyboard_menu import kb_cancel
from keybords.inline.inline_kb_profile import ikb_profile
from loader import dp
from states import register

from utils.db_api import quick_commands as commands


@dp.message_handler(IsPrivate(), text='Указать информацию')
async def register_(message: types.Message, state: FSMContext):
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    await message.delete()
    try:
        user = await commands.select_user(message.from_user.id)

        if user.status == 'active':
            await message.answer(
                f"Привет {message.from_user.first_name}!\n"
                f"Ты уже зарегестрирован!", reply_markup=ikb_profile)
        elif user.status == 'baned':
            await message.answer('Ты забанен')
    except Exception:
        await message.answer('Вы начал регистрацию, \nКого или что ищете?', reply_markup=kb_cancel)
        await register.what.set()


@dp.message_handler(state='*', commands='Отменить')
@dp.message_handler(text='Отменить', state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    try:
        current_state = await state.get_state()
        if current_state is None:
            return

        logging.info('Cancelling state %r', current_state)
        # Cancel state and inform user about it
        await state.finish()
        # And remove keyboard (just in case)
        await message.answer(text='Меню ниже', reply_markup=await kb_menus(message.from_user.id))


    except Exception as ex:
        print(ex)


@dp.message_handler(state=register.what)
async def what_(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 4:
            await state.update_data(what=answer)
            await message.answer(f'Для чего вы здесь?')
            await register.why.set()
        else:
            await message.answer(f'Опишите подробнее')
    except Exception:

        await why_(message, state)


@dp.message_handler(state=register.why)
async def why_(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 4:
            await state.update_data(why=answer)
            await message.answer(f'Напишите ваше Имя')
            await register.first_name.set()
        else:
            await message.answer(f'Опишите подробнее')
    except Exception:

        await first_name_(message, state)


@dp.message_handler(state=register.first_name)
async def first_name_(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 1:
            await state.update_data(first_name=answer)
            await message.answer(f'Напишите вашу Фамилию')
            await register.last_name.set()
        else:
            await message.answer(f'Ведите Имя коректно')
    except Exception:

        await first_name_(message, state)


@dp.message_handler(state=register.last_name)
async def last_name_(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 2:
            await state.update_data(last_name=answer)
            await message.answer(f'Укажите свой город')

            await register.address.set()
        else:
            await message.answer(f'Ведите Фамилию коректно')
    except Exception:
        await last_name_(message, state)


@dp.message_handler(state=register.address)
async def address_(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 2:
            await state.update_data(address=answer)
            await message.answer(f'Укажите вашу организацию')
            await register.corporation.set()
        else:
            await message.answer(f'Ведите название города коректно')
    except Exception:
        await address_(message, state)


@dp.message_handler(state=register.corporation)
async def corporation_(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 4:
            await state.update_data(corporation=answer)
            await message.answer(f'Добавьте аватар')
            await register.avatar.set()
        else:
            await message.answer(f'Ведите название организаци коректно')
    except Exception:
        # await corporation_(message, state)
        await message.answer(f'Добавьте аватар')


async def document_save(files):
    try:
        if files.document.thumb:
            file_id = files.document.thumb.file_id
            url = f'https://api.telegram.org/bot{os.getenv("token")}/getFile?file_id={file_id}'
            resp = requests.get(url)
            img_path = resp.json()['result']['file_path']
            img = requests.get(f'http://api.telegram.org/file/bot{os.getenv("token")}/{img_path}')
            img = Image.open(io.BytesIO(img.content))

            return img
        else:
            return None
    except Exception as ex:
        print(ex)


async def image_save(files):
    file_id = files[0].file_id
    url = f'https://api.telegram.org/bot{os.getenv("token")}/getFile?file_id={file_id}'
    resp = requests.get(url)
    img_path = resp.json()['result']['file_path']
    img = requests.get(f'http://api.telegram.org/file/bot{os.getenv("token")}/{img_path}')
    img = Image.open(io.BytesIO(img.content))
    return img


@dp.message_handler(state=register.avatar, content_types=["photo", 'document'])
async def avatar_(message: types.Message, state: FSMContext):
    try:
        today = datetime.now()
        img = ''
        if os.path.isdir(f"media/{message.from_user.id}"):
            pass
        else:
            os.mkdir(f"media/{message.from_user.id}")

        if message.photo:
            img = await image_save(message.photo)
            img.save(f'media/{message.from_user.id}/{message.photo[0].file_unique_id}.png', format='png')
            path = f'media/{message.from_user.id}/{message.photo[0].file_unique_id}.png'
        else:
            img = await document_save(message)
            img.save(f'media/{message.from_user.id}/{message.document.file_unique_id}.png', format='png')
            path = f'media/{message.from_user.id}/{message.document.file_unique_id}.png'

        answer = path
        if answer:
            await state.update_data(avatar=answer)
            await message.answer(f'Расскажите о себе')
            await register.about.set()
        else:
            await message.answer(f'Пришлите коректный файл')

    except Exception as ex:
        print(ex)
        await corporation_(message, state)


@dp.message_handler(state=register.about)
async def about_(message: types.Message, state: FSMContext):
    try:
        answer = message.text

        if len(answer) > 10:
            await state.update_data(about=answer)
            data = await state.get_data()
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            corporation = data.get('corporation')
            address = data.get('address')
            avatar = data.get('avatar')
            about = data.get('about')
            await commands.add_user(user_id=message.from_user.id,
                                    first_name=first_name,
                                    last_name=last_name,
                                    username=message.from_user.username,
                                    tg_first_name=message.from_user.username,
                                    corporation=corporation,
                                    about=about,
                                    address=address,
                                    avatar=avatar,
                                    status='active'
                                    )
            await message.answer(
                f'Спасибо! {first_name}\n'
                f'Ваши данные были успешно сохранены!', reply_markup=await kb_menus(message.from_user.id ))
            await register.about.set()
            await state.finish()
        else:
            await message.answer(f'Напишите немного больше о себе')
    except Exception as ex:
        await message.answer(f'Чтото пошло не так')
        print(ex)

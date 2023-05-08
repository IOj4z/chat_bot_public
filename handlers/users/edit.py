import io
import os
import requests
from datetime import datetime

from PIL import Image, ImageFilter
from aiogram import types
from aiogram.dispatcher import FSMContext
from keybords.default import kb_menus
from states import edit_state
from loader import dp, bot
from utils.db_api import quick_commands as commands


@dp.callback_query_handler(text='edit_avatar')
async def edit_about(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, 'Пришлити фото для профиля!')

        await edit_state.avatar.set()
    except Exception as ex:
        print(ex)


async def document_save(files):
    try:
        if files.document.thumb:
            file_id = files.document.thumb.file_id
            file_unique_id = files.document.thumb.file_unique_id

            url = f'https://api.telegram.org/bot{os.getenv("token")}/getFile?file_id={file_id}'
            resp = requests.get(url)
            img_path = resp.json()['result']['file_path']
            img = requests.get(f'http://api.telegram.org/file/bot{os.getenv("token")}/{img_path}')
            img = Image.open(io.BytesIO(img.content))

            return img, file_unique_id
        else:
            return None
    except Exception as ex:
        print(ex)


async def image_save(files):
    file_id = files[0].file_id
    file_unique_id = files[0].file_unique_id
    url = f'https://api.telegram.org/bot{os.getenv("token")}/getFile?file_id={file_id}'
    resp = requests.get(url)
    img_path = resp.json()['result']['file_path']
    img = requests.get(f'http://api.telegram.org/file/bot{os.getenv("token")}/{img_path}')
    img = Image.open(io.BytesIO(img.content))
    return img, file_unique_id


@dp.message_handler(state=edit_state.avatar, content_types=["photo", 'document'])
async def corporation_(message: types.Message, state: FSMContext):
    try:
        if message.photo or message.document:
            if os.path.isdir(f"media/{message.from_user.id}"):
                pass
            else:
                os.mkdir(f"media/{message.from_user.id}")

            if message.photo:
                img, file_unique_id = await image_save(message.photo)
                img.save(f'media/{message.from_user.id}/{file_unique_id}.png', format='png')
            else:
                img, file_unique_id = await document_save(message)
                img.save(f'media/{message.from_user.id}/{message.document.file_unique_id}.png', format='png')

            path = f'media/{message.from_user.id}/{file_unique_id}.png'

            answer = path
            if answer is not None:
                user = await commands.select_user(message.from_user.id)
                await commands.update_user_avatar(user_id=user.tg_user_id, avatar=answer)
                await message.answer(f'Вы обновили фото профиля!', reply_markup=await kb_menus(message.from_user.id))
                await state.finish()
            else:
                await message.answer(f'Пришлите коректный фото файл')
                await edit_state.avatar.set()
        else:
            await message.answer(f'Пришлите коректный фото файл')
            await edit_state.avatar.set()


    except Exception as ex:
        print(ex)
        await message.answer(f'Что-то не так')
        await edit_state.avatar.set()


@dp.callback_query_handler(text='edit_about')
async def edit_about(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, 'Ведите текст о себе!')

        await edit_state.about.set()
    except Exception as ex:
        print(ex)


@dp.message_handler(state=edit_state.about)
async def about_(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 10:
            user = await commands.select_user(message.from_user.id)
            await commands.update_user_about(user_id=user.tg_user_id, about=answer)
            await message.answer(f'Вы обновили информацию о себе!', reply_markup=await kb_menus(message.from_user.id))
            await state.finish()
        else:
            await message.answer(f'Напишите немного больше информации о себе!')
    except Exception:
        await message.answer(f'Чтото не так')


@dp.callback_query_handler(text='edit_first_name')
async def edit_first_name(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, 'Ведите имя!')

        await edit_state.first_name.set()
    except Exception as ex:
        print(ex)


@dp.message_handler(state=edit_state.first_name)
async def first_name_(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 2:
            user = await commands.select_user(message.from_user.id)
            await commands.update_user_first_name(user_id=user.tg_user_id, first_name=answer)
            await message.answer(f'Вы обновили имя свое!', reply_markup=await kb_menus(message.from_user.id))
            await state.finish()
        else:
            await message.answer(f'Напишите коректно имя!')
    except Exception:
        await message.answer(f'Чтото не так')


@dp.callback_query_handler(text='edit_last_name')
async def edit_last_name(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, 'Ведите фамилию!')

        await edit_state.last_name.set()
    except Exception as ex:
        print(ex)


@dp.message_handler(state=edit_state.last_name)
async def last_name(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 2:
            user = await commands.select_user(message.from_user.id)
            await commands.update_user_last_name(user_id=user.tg_user_id, last_name=answer)
            await message.answer(f'Вы обновили фамилию свое!', reply_markup=await kb_menus(message.from_user.id, 1))
            await state.finish()
        else:
            await message.answer(f'Напишите коректно фамилия!')
    except Exception:
        await message.answer(f'Чтото не так')


@dp.callback_query_handler(text='edit_corporation')
async def edit_corporation(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, 'Ведите название организации!')

        await edit_state.corporation.set()
    except Exception as ex:
        print(ex)


@dp.message_handler(state=edit_state.corporation)
async def corporation(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 4:
            user = await commands.select_user(message.from_user.id)
            await commands.update_user_corporation(user_id=user.tg_user_id, corporation=answer)
            await message.answer(f'Вы обновили название организации!',
                                 reply_markup=await kb_menus(message.from_user.id))
            await state.finish()
        else:
            await message.answer(f'Напишите коректно название организации!')
    except Exception:
        await message.answer(f'Чтото не так')


@dp.callback_query_handler(text='edit_what')
async def edit_what(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, 'Кого или что ищете?')
        user = await commands.select_user(callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id, f'Было: {user.what}')
        await edit_state.what.set()
    except Exception as ex:
        print(ex)


@dp.message_handler(state=edit_state.what)
async def what(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 4:
            user = await commands.select_user(message.from_user.id)
            await commands.update_user_what(user_id=user.tg_user_id, what=answer)
            await message.answer(f'Вы обновили ответ!',
                                 reply_markup=await kb_menus(message.from_user.id))
            await state.finish()
        else:
            await message.answer(f'Напишите подробнее ваш ответ!')
    except Exception:
        await message.answer(f'Чтото не так')


@dp.callback_query_handler(text='edit_why')
async def edit_why(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, 'Для чего вы здесь?')
        user = await commands.select_user(callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id, f'Было: {user.why}')
        await edit_state.why.set()
    except Exception as ex:
        print(ex)


@dp.message_handler(state=edit_state.why)
async def why(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 4:
            user = await commands.select_user(message.from_user.id)
            await commands.update_user_why(user_id=user.tg_user_id, why=answer)
            await message.answer(f'Вы обновили ответ!',
                                 reply_markup=await kb_menus(message.from_user.id))
            await state.finish()
        else:
            await message.answer(f'Напишите подробнее ваш ответ!')
    except Exception:
        await message.answer(f'Чтото не так')

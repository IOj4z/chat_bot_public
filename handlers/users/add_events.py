import io
import logging
import os
import shutil
from PIL import Image, ImageFilter, PdfParser
from datetime import datetime
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from filters import IsPrivate
from keybords.default import kb_menus
from keybords.default.keyboard_menu import kb_cancel
from loader import dp
from states import events
from states import edit_sevents

from utils.db_api import event_commands
from utils.db_api.quick_commands import select_user


@dp.message_handler(IsPrivate(), text='Создать мероприятие')
async def add_events_(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer('Вы начал создовать мероприятие, \nВедите название мероприятие:', reply_markup=kb_cancel)
    await events.name.set()


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


@dp.message_handler(state=events.name)
async def events_name_(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 4:
            await state.update_data(name=answer)
            await message.answer(f'Напишите описание: ')
            await events.desc.set()
        else:
            await message.answer(f'Опишите подробнее')
    except Exception as ex:
        print(ex)
        await events_desc_(message, state)


@dp.message_handler(state=events.desc)
async def events_desc_(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 4:
            await state.update_data(desc=answer)
            await message.answer(f'Пришлите обложку для мероприятие: ')
            await events.cover.set()
        else:
            await message.answer(f'Опишите подробнее')
    except Exception:

        await events_cover_(message, state)


async def document_save(files):
    try:
        if files.document.thumb:
            print(files)
            file_id = files.document.file_id
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


async def document_file_save(files):
    try:
        if files.document.thumb:
            print(files)
            await files.document.download(f'file/{files.from_user.id}/{files.document.file_name}')
            img = f'file/{files.from_user.id}/{files.document.file_name}'
            return img
        else:
            return None
    except Exception as ex:
        print(ex)


async def image_save(files):
    file_id = files[2].file_id
    url = f'https://api.telegram.org/bot{os.getenv("token")}/getFile?file_id={file_id}'
    resp = requests.get(url)
    img_path = resp.json()['result']['file_path']
    img = requests.get(f'http://api.telegram.org/file/bot{os.getenv("token")}/{img_path}')
    img = Image.open(io.BytesIO(img.content))
    return img


@dp.message_handler(state=events.cover, content_types=["photo", 'document'])
async def events_cover_(message: types.Message, state: FSMContext):
    try:
        img = ''
        if os.path.isdir(f"cover/{message.from_user.id}"):
            pass
        else:
            os.mkdir(f"cover/{message.from_user.id}")

        if message.photo:
            img = await image_save(message.photo)
            print(message.photo)
            img.save(f'cover/{message.from_user.id}/{message.photo[2].file_unique_id}.png', format='png')
            path = f'cover/{message.from_user.id}/{message.photo[2].file_unique_id}.png'
        else:
            img = await document_save(message)
            img.save(f'cover/{message.from_user.id}/{message.document.file_unique_id}.png', format='png')
            path = f'cover/{message.from_user.id}/{message.document.file_unique_id}.png'

        answer = path
        if answer:
            await state.update_data(cover=answer)
            await message.answer(f'Напишите время начала(формате: 31-12-2023 23-59-59): ')
            await events.date.set()
        else:
            await message.answer(f'Пришлите коректный файл')

    except Exception as ex:
        print(ex)
        await events_cover_(message, state)


@dp.message_handler(state=events.date)
async def events_date_(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if len(answer) > 4:
            await state.update_data(date=answer)
            await message.answer(f'Пришлите файл мероприятие (pdf, pptx, jpg)')
            await events.file.set()
        else:
            await message.answer(f'Пришлите коректно дату')
    except Exception:

        await events_date_(message, state)


@dp.message_handler(state=events.file, content_types=["photo", 'document'])
async def events_file_(message: types.Message, state: FSMContext):
    try:
        answer = message.document
        if message.document:
            if os.path.isdir(f"file/{message.from_user.id}"):
                pass
            else:
                os.mkdir(f"file/{message.from_user.id}")

            path = await document_file_save(message)

            await state.update_data(file=path)
            await message.answer(f'Пришлите программу мероприятие')
            await events.program.set()
        else:
            await message.answer(f'Пришлите коректно файл (pdf, pptx, jpg)')
    except Exception:
        await events_file_(message, state)


@dp.message_handler(state=events.program)
async def events_program_(message: types.Message, state: FSMContext):
    try:
        answer = message.text

        if len(answer) > 10:
            await state.update_data(program=answer)
            data = await state.get_data()
            name = data.get('name')
            desc = data.get('desc')
            date = data.get('date')
            cover = data.get('cover')
            file = data.get('file')
            program = data.get('program')
            user = await select_user(message.from_user.id)

            await event_commands.add_events(
                name=name,
                desc=desc,
                date=date,
                cover=cover,
                file=file,
                program=program,
                user_id=user.id,
            )
            await message.answer(
                f'Спасибо! {name}\n'
                f'Мероприятие успешно создано!', reply_markup=await kb_menus(message.from_user.id))

            await state.finish()
    except Exception as ex:
        await message.answer(f'Чтото пошло не так')
        print(ex)

from aiogram.types import ContentType, Message, InputFile, MediaGroup

from loader import dp


@dp.message_handler(content_types=ContentType.PHOTO)
async def send_photo_file_id(message: Message):
    await message.reply(message.photo[-1].file_id)
    print(message.photo)


@dp.message_handler(content_types=ContentType.VIDEO)
async def send_video_file_id(message: Message):
    await message.reply(message.video.file_id)


@dp.message_handler(text='/photo')
async def send_photo(message: Message):
    chat_id = message.from_user.id

    photo_file_id = 'AgACAgIAAxkBAAIBNmQvuHRWybSmmiQLX4ASRKwVbfa-AAJwyDEbHc14SfpVPEJbdR1GAQADAgADeAADLwQ'
    photo_url = 'sd'
    photo_bytes = InputFile(path_or_bytesio='media/Screenshot-20230407121345-377x700.png')

    await dp.bot.send_photo(chat_id=chat_id, photo=photo_bytes)
    await dp.bot.send_video(chat_id=chat_id, video=photo_file_id)


@dp.message_handler(text='/album')
async def send_album(message: Message):
    album = MediaGroup()
    photo_file_id = 'AgACAgIAAxkBAAIBNmQvuHRWybSmmiQLX4ASRKwVbfa-AAJwyDEbHc14SfpVPEJbdR1GAQADAgADeAADLwQ'
    album.attach_photo(photo=photo_file_id, caption='ID photo')
    photo_bytes = InputFile(path_or_bytesio='media/Screenshot-20230407121345-377x700.png')
    album.attach_photo(photo=photo_bytes, caption='byte photo')
    await message.answer_media_group(media=album)

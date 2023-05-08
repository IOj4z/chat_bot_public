from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_file = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Получить файлы', callback_data='Получить файлы')
                                    ]
                                ])

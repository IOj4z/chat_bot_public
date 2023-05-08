from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_profile = InlineKeyboardMarkup(row_width=1,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(text='Мой профиль', callback_data='profile'),
                                       ],
                                       [
                                           InlineKeyboardButton(text='Нетворкинг', callback_data='Нетворкинг'),
                                       ],
                                       [
                                           InlineKeyboardButton(text='Прошедшие мероприятия',
                                                                callback_data='Прошедшие мероприятия'),
                                           InlineKeyboardButton(text='Будущие мероприятия',
                                                                callback_data='Будущие мероприятия'),

                                       ],
                                   ])

ikb_profile_edit = InlineKeyboardMarkup(row_width=1,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text='Имя', callback_data='edit_first_name'),
                                                InlineKeyboardButton(text='Фамилия', callback_data='edit_last_name'),
                                            ],
                                            [

                                                InlineKeyboardButton(text='Организация', callback_data='edit_corporation'),
                                                InlineKeyboardButton(text='О себе', callback_data='edit_about'),
                                            ],
                                            [
                                                InlineKeyboardButton(text='Фото', callback_data='edit_avatar'),

                                            ],
                                            [
                                                InlineKeyboardButton(text='Для чего вы здесь?', callback_data='edit_why'),
                                            ],
                                            [
                                                InlineKeyboardButton(text='Кого или что ищете?', callback_data='edit_what'),
                                            ]

                                        ])

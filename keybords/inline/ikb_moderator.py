from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_my = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[

                                    [
                                        InlineKeyboardButton(text='Мои мероприятие',
                                                             switch_inline_query_current_chat='Мои'),
                                    ],
                                ])


ikb_back = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[

                                    [
                                        InlineKeyboardButton(text='Назад',
                                                             callback_data='Назад'),
                                    ],

                                ])
ikb_my_event_edit = InlineKeyboardMarkup(row_width=1,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text='Название', callback_data='edit_my_event_name'),
                                                InlineKeyboardButton(text='Описание', callback_data='edit_my_event_desc'),
                                            ],
                                            [

                                                InlineKeyboardButton(text='Программа', callback_data='edit_my_event_program'),
                                                InlineKeyboardButton(text='Дата', callback_data='edit_my_event_date'),
                                            ],
                                            [
                                                InlineKeyboardButton(text='Обложка', callback_data='edit_my_event_cover'),

                                            ]

                                        ])

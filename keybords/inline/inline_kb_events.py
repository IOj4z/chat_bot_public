from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_last = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[

                                    [
                                        InlineKeyboardButton(text='Открыть',
                                                             switch_inline_query_current_chat='Прошедшие'),
                                    ],
                                ])
ikb_future = InlineKeyboardMarkup(row_width=1,
                                  inline_keyboard=[

                                      [
                                          InlineKeyboardButton(text='Открыть',
                                                               switch_inline_query_current_chat='Будущие'),
                                      ],
                                  ])
ikb_back = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[

                                    [
                                        InlineKeyboardButton(text='Назад',
                                                             callback_data='Назад'),
                                    ],

                                ])

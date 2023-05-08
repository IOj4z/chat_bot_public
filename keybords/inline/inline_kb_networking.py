from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_networking = InlineKeyboardMarkup(row_width=2,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text='Нетворкинг', callback_data='get_networking'),
                                              InlineKeyboardButton(text='Принять участие', callback_data='submit'),
                                              InlineKeyboardButton(text='Получить файлы', callback_data='get_file')
                                          ],
                                      ])

ikb_last_networking = InlineKeyboardMarkup(row_width=2,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text='Нетворкинг', callback_data='get_networking'),
                                              InlineKeyboardButton(text='Получить файлы', callback_data='get_file')
                                          ],
                                      ])

ikb_mem_networking = InlineKeyboardMarkup(row_width=2,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text='Нетворкинг',
                                                                   switch_inline_query_current_chat='Нетворкинг'),
                                          ],
                                      ])

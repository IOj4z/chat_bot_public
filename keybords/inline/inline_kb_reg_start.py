from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_reg_start = InlineKeyboardMarkup(row_width=2,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(text='Указать информацию',
                                                                  callback_data='Указать информацию'),
                                         ],
                                         [
                                             InlineKeyboardButton(text='Отменить', callback_data='Отменить'),
                                         ],

                                     ])

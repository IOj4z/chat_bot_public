from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Мой профиль', callback_data='Мой профиль'),
                                        # InlineKeyboardButton(text='Сылка', url='https://youtu.be/2Il_Ab-s0W8?list'
                                        #                                        '=PLPELDof3v08efHGT3gVLPCXG5cKRo50Nn&t=219'),
                                    ],
                                    [
                                        InlineKeyboardButton(text='Редактировать', callback_data='Редактировать')
                                    ],
                                    # [
                                    #     InlineKeyboardButton(text='Заменить кнопки меню', callback_data='Кнопки2')
                                    # ]
                                ])

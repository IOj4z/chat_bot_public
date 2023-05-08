from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

btns = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Нажмите на кнопку",
)
btns.add(KeyboardButton(text="Указать информацию"))
btns.add(KeyboardButton(text="Отменить"))


ink = InlineKeyboardMarkup(row_width=2)
inb1 = InlineKeyboardButton(text='Указать информацию')
inb2 = InlineKeyboardButton(text='Мой профиль')
inb3 = InlineKeyboardButton(text='Редактировать')

inb4 = InlineKeyboardButton(text='Прошедшие мероприятия')
inb5 = InlineKeyboardButton(text='Нетворкинг')
inb6 = InlineKeyboardButton(text='Будущие мероприятия')

inb7 = InlineKeyboardButton(text='Принять участие')
inb8 = InlineKeyboardButton(text='Присутствовать очно')
inb9 = InlineKeyboardButton(text='Присутствовать дистанционно')

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Домашняя Работа').add('Расписание звонков').add('Расписание занятий')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Домашняя Работа').add('Расписание звонков').add('Расписание занятий').add('Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить дз')

catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text='Русский язык', callback_data='r-lan'),
                 InlineKeyboardButton(text='Математика', callback_data='math'),
                 InlineKeyboardButton(text='География', callback_data='geog')),
                 # InlineKeyboardButton(text='Истрория', callback_data='history')),
                 # InlineKeyboardButton(text='Информатика', callback_data='OBZH')),
                 # InlineKeyboardButton(text='Информатика', callback_data='phis')),




cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('Отмена')
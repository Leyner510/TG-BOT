import sqlite3

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from app import keyboards as kb
from app import database as db

#from dotenv import load_dotenv
import os

storage = MemoryStorage()
#load_dotenv()
bot = Bot('6932608380:AAEgm1JTjb5LoJM34uLAfNkAjcdj3t7cHsQ')
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен!')

class NewOrder(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    await message.answer_sticker('CAACAgIAAxkBAAMpZBAAAfUO9xqQuhom1S8wBMW98ausAAI4CwACTuSZSzKxR9LZT4zQLwQ')
    await message.answer(f'{message.from_user.first_name}, привет дорогой одногруппник!',
                         reply_markup=kb.main)
    if message.from_user.id == 1463745223:
        await message.answer('Вы авторизовались как администратор!', reply_markup=kb.main_admin)


@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')


@dp.message_handler(text='Домашняя Работа')
async def catalog(message: types.Message):
    await message.answer('Выберите категорию', reply_markup=kb.catalog_list)




@dp.message_handler(text='Расписание звонков')
async def cart(message: types.Message):
    await message.answer('Пока ничего нет')


@dp.message_handler(text='Расписание занятий')
async def contacts(message: types.Message):
    await message.answer('Пока ничего нет')


@dp.message_handler(text='Админ-панель')
async def contacts(message: types.Message):
    if message.from_user.id == 1463745223:
        await message.answer('Вы вошли в админ-панель', reply_markup=kb.admin_panel)
    else:
        await message.reply('Я тебя не понимаю.')


@dp.message_handler(text='Добавить дз')
async def add_item(message: types.Message):
    if message.from_user.id == 1463745223:
        await NewOrder.type.set()
        await message.answer('Выберите предмет', reply_markup=kb.catalog_list)
    else:
        await message.reply('Я тебя не понимаю.')


@dp.callback_query_handler(state=NewOrder.type)
async def add_item_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer('Напишите тему Дз', reply_markup=kb.cancel)
    await NewOrder.next()


@dp.message_handler(state=NewOrder.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Напишите по какому предмету')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer('Напишите само дз')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.price)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Отправьте фотографию домашней работы(если нет фото дз, скинь мем)')
    await NewOrder.next()


@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def add_item_photo_check(message: types.Message):
    await message.answer('Это не фотография!')


@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await db.add_item(state)
    await message.answer('Дз успешно создано!', reply_markup=kb.admin_panel)
    await state.finish()


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю.')

# @dp.callback_query_handler(func=lambda call : True)
# def callback(call):
#     conn = sqlite3.connect('tg.bd')
#     cur = conn.cursor()
#
#     cur.execute('SELECT * FROM items')
#     items = cur.fetchall()
#
#     info = ''
#     for el in items:
#         info += f'Тема: {el[1]}, Предмет: {el[2]}, Задание: {el[3]}, Фото задания: {el[4]}'
#
#     cur.close()
#     conn.close()
#
#     bot.send_message(call.message.chat.id, info)


@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == 'r-lan':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали Русский язык')
    elif callback_query.data == 'math':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали Математику')
    elif callback_query.data == 'geog':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали Географию')
    # elif callback_query.data == 'history':
    #     await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали Историю')
    # elif callback_query.data == 'OBZH':
    #     await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали ОБЖ')
    # elif callback_query.data == 'phis':
    #     await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали Физику')
    # elif callback_query.data == 'chemistry':
    #     await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали Химию')
    # elif callback_query.data == 'litra':
    #     await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали Литертуру')
    # elif callback_query.data == 'an-lan':
    #     await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали Ин.Яз')
    #

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
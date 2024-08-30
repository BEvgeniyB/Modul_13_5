from config import api
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
# import asyncio


bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton(text="Рассчитать")
button2 = types.KeyboardButton(text="Информация")
kb.row(button1,button2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weigth = State()


def m_cg_for_women(data):
    calories = (10 * float(data['weigth']) + 6.25 * float(data['growth']) -
                5 * float(data['age']) - float(161))
    return calories

@dp.message_handler(commands='start')
async def starter(message: types.Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.',reply_markup= kb)

@dp.message_handler(text="Информация")
async def set_age(message: types.Message):
    await message.answer('Расчет ведется по формуле Миффлина - Сан Жеора')


@dp.message_handler(text="Рассчитать")
async def set_age(message: types.Message):
            await message.answer('Введите свой возраст:')
            await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост в сантиметрах:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weigth.set()


@dp.message_handler(state=UserState.weigth)
async def set_weight(message, state):
    await state.update_data(weigth=message.text)
    data = await state.get_data()
    await state.finish()
    await  message.answer(f'Суточная норма калорий равна : {m_cg_for_women(data)}')
    await message.answer('Введите команду /start, чтобы начать расчет.')

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

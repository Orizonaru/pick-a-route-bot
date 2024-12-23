from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BotCommand
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import pandas as pd
from request_weather import RequestWeather
from create_plots import create_plots
from aiogram.types.input_file import BufferedInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_days_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 день", callback_data="1")],
        [InlineKeyboardButton(text="3 дня", callback_data="3")],
        [InlineKeyboardButton(text="5 дней", callback_data="5")]
    ])
    return keyboard

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/help", description="Помощь по боту"),
        BotCommand(command="/weather", description="Получить прогноз погоды"),
    ]
    await bot.set_my_commands(commands)

async def main():
    bot = Bot(token='7796197819:AAFhDd6qMr82x1LYJzt9fES-syUQOETObbM')
    dp = Dispatcher(storage=MemoryStorage())

    class WeatherFSM(StatesGroup):
        city_array = State()
        days_selection = State()
        confirm_route = State()

    @dp.message(Command("start"))
    async def message_start(message: types.Message):
        await message.reply("Привет! Я бот для прогноза погоды. Используйте команду /weather для получения прогноза.")

    @dp.message(Command("help"))
    async def message_help(message: types.Message):
        await message.reply(
            "Доступные команды:\n/start - Начать работу\n/help - Помощь\n/weather - Получить прогноз погоды")

    @dp.message(Command("weather"))
    async def message_weather(message: types.Message, state: FSMContext):
        await message.answer("Введите города, которые вы хотели бы посетить через запятую:")
        await state.set_state(WeatherFSM.city_array)

    @dp.message(WeatherFSM.city_array)
    async def process_end_location(message: types.Message, state: FSMContext):
        await state.update_data(city_array=message.text)
        await message.answer(
            "На сколько дней хотите получить прогноз? Возможен прогноз от 1 до 5 дней",
            reply_markup=get_days_keyboard()
        )
        await state.set_state(WeatherFSM.days_selection)

    @dp.callback_query(lambda call: call.data.isdigit())
    async def select_days(call: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        city_array = list(map(lambda x: x.strip(), data['city_array'].split(',')))
        n_days = int(call.data)

        try:
            requested_days = 5

            def weather_validation(temp_max, temp_min, wind_speed, rain_prob):
                if temp_max > 35 or temp_min < -10 or wind_speed > 50 or rain_prob > 80:
                    return False
                else:
                    return True

            weather_client = RequestWeather(api_key='vlpOC4ZROyMdSgTi0L7cn3vNsXifcgpB', language="ru-ru")

            def get_city_weather(city_name):
                autocomplete_results = weather_client.fetch_city_autocomplete(city_name)
                if not autocomplete_results:
                    return None
                location_code = autocomplete_results[0]["Key"]
                print(city_array)
                forecast = weather_client.fetch_daily_forecast(forecast_days=requested_days,
                                                               location_code=location_code)[0:n_days]
                print(forecast)
                return_data = {"day": [day for day in range(1, n_days + 1)],
                               "temp_max": [],
                               "temp_min": [],
                               "wind_speed": [],
                               "rain_prob": [],
                               "is_good": []}
                for day in range(len(forecast)):
                    return_data["temp_max"].append(forecast[day]["temp_max"])
                    return_data["temp_min"].append(forecast[day]["temp_min"])
                    return_data["wind_speed"].append(forecast[day]["wind_speed"])
                    return_data["rain_prob"].append(forecast[day]["rain_prob"])
                    return_data["is_good"].append(
                        weather_validation(forecast[day]["temp_max"], forecast[day]["temp_min"],
                                           forecast[day]["wind_speed"],
                                           forecast[day]["rain_prob"]))
                print(return_data)
                return return_data

            data = {}
            for i in city_array:
                data[i] = pd.DataFrame(get_city_weather(i))
            plots = create_plots(data)
            print('Plots created')
            decoded_plots = [BufferedInputFile(plots[i].getvalue(), filename=f"{i}.png") for i in range(len(plots))]
            for i in decoded_plots:
                await call.message.answer_photo(photo=i)

        except Exception as e:
            await call.message.answer(f"❌ Ошибка: {e}")
        finally:
            await state.clear()


    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
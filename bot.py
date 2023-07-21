import requests
import datetime
from config import tg_bot_token, open_weather_token

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)

# диспетчер для управления ботом
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Hello! Write me the name of the city and I will send a weather report!")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        params = {'q': message.text,
                  'appid': open_weather_token,
                  'units': 'metric',
                  'format': 'json'}

        response_weather = requests.get("http://api.openweathermap.org/data/2.5/weather", params=params)
        data = response_weather.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Weird weather!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"City weather: {city}\nTemperature: {cur_weather}C° {wd}\n"
                            f"Humidity: {humidity}%\nPressure: {pressure}\nWind: {wind} m/s\n"
                            f"Sunrise: {sunrise_timestamp}\nSunset: {sunset_timestamp}\nDay length: {length_of_the_day}\n"
                            )
    except:
        await message.reply("\U00002620 Check city name \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)

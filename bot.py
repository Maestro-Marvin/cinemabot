import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from config import Config
from database import Database
from search_api import MovieSearchAPI
from datetime import datetime
from logger import logger, log_message, log_error

logging.basicConfig(level=logging.INFO)

config = Config()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
db = Database(config.DB_PATH)
movie_api = MovieSearchAPI()

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я бот для поиска фильмов."
        "Просто напиши название фильма, и я найду где его посмотреть!\n\n"
        "Доступные команды:\n"
        "/help - показать список команд\n"
        "/history - показать историю поиска\n"
        "/stats - показать статистику по фильмам"
    )

@dp.message(Command('help'))
async def send_help(message: types.Message):
    await message.reply(
        "/history - показать историю поиска\n"
        "/stats - показать статистику поиска"
    )

@dp.message(Command('history'))
async def show_history(message: types.Message):
    history = await db.get_search_history(message.from_user.id)
    if not history:
        await message.reply("История поиска пуста")
        return

    text = "История поиска:\n\n"
    for query, date in history:
        text += f"🔍 {query} - {date}\n"
    
    await message.reply(text)

@dp.message(Command('stats'))
async def show_stats(message: types.Message):
    stats = await db.get_movie_stats(message.from_user.id)
    if not stats:
        await message.reply("Статистика пуста")
        return

    text = "Статистика поиска:\n\n"
    for movie_title, count in stats:
        text += f"🎬 {movie_title}: {count} раз(а)\n"
    
    await message.reply(text)

@dp.message(F.text)
async def search_movie(message: types.Message):
    try:
        user_id = message.from_user.id
        query = message.text
        log_message(user_id, f"Searching for: {query}")
        
        await db.add_search_history(user_id, query)
        
        link = await movie_api.search_movie(query)
        if not link:
            await message.reply(
                "К сожалению, я не смог найти ссылки на этот фильм 😢\n"
                "Попробуйте изменить запрос или поискать другой фильм."
            )
            return

        await db.update_movie_stats(user_id, link, query)

        text = f"🎬 Результаты поиска для \"{query}\":\n\n"
        text += f"{link}\n\n"

        await message.reply(text)
        log_message(user_id, f"Successfully sent {len(link)} links")
        
    except Exception as e:
        log_error(e, "search_movie")
        await message.reply(
            "Произошла ошибка при поиске фильма 😢\n"
            "Пожалуйста, попробуйте позже."
        )

async def main():
    await db.init()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = os.environ['BOT_TOKEN']
    CX = os.environ['CX']
    API_KEY = os.environ['GOOGLE_API_KEY']
    DB_PATH: str = 'cinema_bot.db'

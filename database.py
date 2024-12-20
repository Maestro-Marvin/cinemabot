import aiosqlite
from datetime import datetime

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            with open('schema.sql', 'r') as f:
                await db.executescript(f.read())
            await db.commit()

    async def add_search_history(self, user_id: int, query: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'INSERT INTO search_history (user_id, query) VALUES (?, ?)',
                (user_id, query)
            )
            await db.commit()

    async def get_search_history(self, user_id: int) -> list:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                'SELECT query, search_date FROM search_history WHERE user_id = ? ORDER BY search_date DESC LIMIT 10',
                (user_id,)
            ) as cursor:
                return await cursor.fetchall()

    async def update_movie_stats(self, user_id: int, movie_id: str, movie_title: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO movie_stats (user_id, movie_id, movie_title)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id, movie_id) 
                DO UPDATE SET shown_count = shown_count + 1
            ''', (user_id, movie_id, movie_title))
            await db.commit()

    async def get_movie_stats(self, user_id: int) -> list:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                'SELECT movie_title, shown_count FROM movie_stats WHERE user_id = ? ORDER BY shown_count DESC',
                (user_id,)
            ) as cursor:
                return await cursor.fetchall() 
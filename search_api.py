import aiohttp
from typing import Optional, Dict, List
from config import Config
import asyncio
from logger import logger, log_error

config = Config()
sources = ['вк', 'rutube']
domains = ['vk.com/video', 'rutube.ru/video']


class MovieSearchAPI:
    def __init__(self):
        self.search_url = "https://www.googleapis.com/customsearch/v1"
        self.api_key = config.API_KEY
        self.cx = config.CX
        self.sources = sources
        self.domains = domains

    async def search_movie(self, query: str) -> Optional[str]:
        """Асинхронный поиск фильма по всем источникам"""
        try:
            tasks = [
                self.search_movie_by_source(query, source)
                for source in self.sources
            ]
            
            results = await asyncio.gather(*tasks)
            
            all_links = []
            for links in results:
                if links:
                    all_links.extend(links)
            
            logger.info(f"Found {len(all_links)} links for query: {query}")
            return all_links[0] if all_links else None
            
        except Exception as e:
            log_error(e, "search_movie")
            return None

    async def search_movie_by_source(self, query: str, source: str) -> List[str]:
        """Поиск фильма в конкретном источнике"""
        try:
            search_query = f"фильм {query} смотреть {source}"
            logger.info(f"Searching in {source}: {search_query}")

            params = {
                'key': self.api_key,
                'cx': self.cx,
                'q': search_query,
                'num': 10
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.search_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        links = self._extract_links(data)
                        logger.info(f"Found {len(links)} links in {source}")
                        return links
                    else:
                        logger.error(f"Search in {source} failed with status {response.status}")
                        
        except Exception as e:
            log_error(e, f"search_movie_by_source ({source})")
        
        return []

    def _extract_links(self, data: Dict) -> List[str]:
        """Извлекает ссылки из ответа Google API"""
        links = []
        
        if 'items' in data:
            for item in data['items']:
                link = item.get('link', '')
                if any(domain in link.lower() for domain in self.domains):
                    links.append(link)
        return links
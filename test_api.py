import asyncio
from config import Config
from search_api import MovieSearchAPI
from logger import logger

async def test_search(query: str):
    api = MovieSearchAPI()
    
    logger.info(f"Testing search for: {query}")
    result = await api.search_movie(query)
    
    if result:
        logger.info("Search result:")
        logger.info("Link:")
        logger.info(f"- {result}")
    else:
        logger.error("No results found")

if __name__ == "__main__":
    test_queries = [
        "как витька чеснок вез леху штыря в дом инвалидов"
    ]
    
    for query in test_queries:
        asyncio.run(test_search(query)) 
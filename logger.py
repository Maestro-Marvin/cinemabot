import logging
from datetime import datetime

# Настраиваем формат логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('cinema_bot')

def log_message(user_id: int, message: str):
    logger.info(f"User {user_id}: {message}")

def log_error(error: Exception, context: str = ""):
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)

def log_api_response(method: str, response: dict):
    logger.debug(f"API {method} response: {response}") 
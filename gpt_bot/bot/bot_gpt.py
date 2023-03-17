import logging
import os
import tiktoken

from telegram.ext import ApplicationBuilder, filters, MessageHandler
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def num_tokens_from_string(string: str, encoding_model: str) -> int:
    """Возвращает количество токенов в строке."""
    encoding = tiktoken.encoding_for_model(encoding_model)
    num_tokens = len(encoding.encode(string))
    return num_tokens

async def echo(update, context):
    """Отправляет ответ на текстовое входящее сообщение."""
    chat = update.effective_chat
    role = 'user'
    content = update.effective_message.text
    content_tokens = num_tokens_from_string(content, 'gpt-3.5-turbo')

    await update.message.reply_text(f'Тестируем бота. Должно быть {content_tokens}')

application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
echo_handler = MessageHandler(filters.TEXT, echo)
application.add_handler(echo_handler)
application.run_polling()

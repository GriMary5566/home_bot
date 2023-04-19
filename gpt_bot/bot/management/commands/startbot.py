import logging
import os

from django.core.management.base import BaseCommand
from telegram.ext import ApplicationBuilder, filters, MessageHandler
from dotenv import load_dotenv

from bot.bot_gpt import echo

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Запускает телеграмбота.'

    def handle(self, *args, **options):
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        echo_handler = MessageHandler(filters.TEXT, echo)
        application.add_handler(echo_handler)
        application.run_polling()

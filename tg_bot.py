import logging
import os
import random

from dotenv import load_dotenv
from telegram.ext import Filters
from telegram.ext import MessageHandler, CommandHandler
from telegram.ext import Updater

from answering_machine import AnsweringMachine
from tg_log_handler import BotLogsHandler

logger = logging.getLogger('TelegramPublishingBot')


class TelegramHelperBot(object):
    def __init__(self, token, answering_machine, proxy_url=None):

        request_kwargs = None
        if proxy_url is not None:
            request_kwargs = {
                'proxy_url': proxy_url,
            }
        self.updater = Updater(token=token, request_kwargs=request_kwargs)
        start_command_handler = CommandHandler('start', self.handle_start)
        message_handler = MessageHandler(Filters.text, self.handle_message)
        self.updater.dispatcher.add_handler(start_command_handler)
        self.updater.dispatcher.add_handler(message_handler)

        self.answering_machine = answering_machine
        self.session_id_prefix = '1'

    def get_session_id(self, update):
        return int(self.session_id_prefix + str(update.message.chat_id))

    def start(self):
        self.updater.start_polling()
        logger.info('Bot started.')

    @staticmethod
    def handle_start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text='Здравствуйте!')

    def handle_message(self, bot, update):
        message = update.message.text
        session_id = self.get_session_id(update)
        answer = self.answering_machine.get_answer(message, session_id)
        logger.debug(f'For message - {str(message)}, got answer - {str(answer)}.')
        if answer is not None:
            bot.send_message(chat_id=update.message.chat_id, text=answer)


if __name__ == '__main__':
    load_dotenv()
    telegram_helper_bot_token = os.getenv('TELEGRAM_HELPER_BOT_TOKEN')
    telegram_log_bot_token = os.getenv("TELEGRAM_LOG_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    proxy_url = os.getenv('TELEGRAM_PROXY_URL', None)
    google_project_id = os.getenv('GOOGLE_PROJECT_ID')

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    bot_handler = BotLogsHandler(level=logging.INFO, telegram_token=telegram_log_bot_token,
                                 proxy_url=proxy_url, chat_id=chat_id)
    bot_handler.setFormatter(formatter)
    logger.addHandler(bot_handler)

    try:
        answering_machine = AnsweringMachine(
            project_id=google_project_id,
            language_code='ru'
        )
        bot = TelegramHelperBot(
            token=telegram_helper_bot_token,
            answering_machine=answering_machine,
            proxy_url=proxy_url
        )
        bot.start()
    except Exception as err:
        logger.error("Unexpected error occurred:")
        logger.error(err, exc_info=True)

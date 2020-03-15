import logging
import os
import random

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from answering_machine import AnsweringMachine
from tg_log_handler import BotLogsHandler

logger = logging.getLogger('VKPublishingBot')


class VkHelperBot(object):
    def __init__(self, token, answering_machine):

        self.vk_session = vk_api.VkApi(token=token)
        self.vk_api = self.vk_session.get_api()
        self.longpoll = VkLongPoll(self.vk_session)

        self.answering_machine = answering_machine

    def start(self):
        logger.info('Starting to listen for new messages.')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.handle_message(event)

    def handle_message(self, event):
        message = event.text
        answer = self.answering_machine.get_answer(message, ignore_unrecognized=True)
        logger.debug(f'For message - {str(message)}, got answer - {str(answer)}.')
        if answer is not None:
            self.vk_api.messages.send(user_id=event.user_id, message=answer, random_id=random.randint(1, 1000))


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('VK_GROUP_TOKEN')
    google_project_id = os.getenv('GOOGLE_PROJECT_ID')
    telegram_log_bot_token = os.getenv("TELEGRAM_LOG_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    proxy_url = os.getenv('TELEGRAM_PROXY_URL', None)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    bot_handler = BotLogsHandler(level=logging.INFO, telegram_token=telegram_log_bot_token,
                                 proxy_url=proxy_url, chat_id=chat_id)
    bot_handler.setFormatter(formatter)
    logger.addHandler(bot_handler)

    try:
        answering_machine = AnsweringMachine(
            project_id=google_project_id,
            session_id=random.randint(0, 9999),
            language_code='ru'
        )
        bot = VkHelperBot(
            token=token,
            answering_machine=answering_machine
        )
        bot.start()
    except Exception as err:
        logger.error("Unexpected error occurred:")
        logger.error(err, exc_info=True)

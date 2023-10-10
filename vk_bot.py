import logging
import random

import telegram
from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dialogflow import detect_intent_texts


class TelegramLogHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record):
        log_message = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_message)


def send_message(user_id, text, vk_api):
    try:
        vk_api.messages.send(
            user_id=user_id,
            message=text,
            random_id=random.randint(1, 1000)
        )
    except Exception as e:
        bot.logger.exception(f'Произошла ошибка: {e}')


def main():
    env = Env()
    env.read_env()
    chat_id = env('CHAT_ID')
    telegram_token = env('TELEGRAM_TOKEN')
    bot = telegram.Bot(token=telegram_token)
    bot.logger.addHandler(TelegramLogHandler(bot, chat_id))
    bot.logger.warning('vk - Бот запущен')
    vk_token = env('VK_TOKEN')
    project_id = env('PROJECT_ID')
    try:
        vk_session = vk.VkApi(token=vk_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                session_id = f'vk-{event.user_id}'
                user_message = event.text
                text = detect_intent_texts(session_id, event.text, project_id)
                if text is None:
                    bot.logger.info(f'Сообщение пользователя: {user_message}')
                else:
                    send_message(event.user_id, text, vk_api)

    except Exception as e:
        bot.logger.exception(f'Произошла ошибка: {e}')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    main()

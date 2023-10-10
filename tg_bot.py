import logging

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from environs import Env
from dialogflow import detect_intent_texts


class TelegramLogHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record):
        log_message = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_message)


def start(update, context):
    user = update.effective_user
    update.message.reply_markdown_v2(f'Здравствуйте {user.mention_markdown_v2()}')


def main():
    env = Env()
    env.read_env()
    project_id = env('PROJECT_ID')
    chat_id = env('CHAT_ID')
    telegram_token = env('TELEGRAM_TOKEN')
    bot = telegram.Bot(token=telegram_token)
    bot.logger.addHandler(TelegramLogHandler(bot, chat_id))
    bot.logger.warning('tg - Бот запущен')

    def handle_text(update, context):
        try:
            session_id = f'tg-{update.message.from_user.id}'
            text = update.message.text
            bot_response = detect_intent_texts(str(session_id), text, project_id)
            if bot_response:
                update.message.reply_text(bot_response)
            else:
                update.message.reply_text("Извините, не могу понять ваш запрос.")
        except Exception as e:
            bot.logger.exception(f'Произошла ошибка: {e}')

    updater = Updater(env('TG_TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

import logging

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from environs import Env
from dialogflow import detect_intent_texts
from TelegramLogHandler import TelegramLogHandler


def start(update, context):
    user = update.effective_user
    update.message.reply_markdown_v2(f'Здравствуйте {user.mention_markdown_v2()}')


def handle_text(update, context, project_id):
    session_id = f'tg-{update.message.from_user.id}'
    text = update.message.text
    text_answer, fallback = detect_intent_texts(str(session_id), text, project_id)
    if text_answer:
        update.message.reply_text(text_answer)
    else:
        update.message.reply_text(fallback)


def main():
    try:
        env = Env()
        env.read_env()
        project_id = env('PROJECT_ID')
        chat_id = env('CHAT_ID')
        telegram_token = env('TELEGRAM_TOKEN')
        bot = telegram.Bot(token=telegram_token)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
        bot.logger.addHandler(TelegramLogHandler(bot, chat_id))
        bot.logger.warning('tg - Бот запущен')

        updater = Updater(env('TG_TOKEN'))
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,
                                              lambda update, context: handle_text(update, context, project_id)))

        updater.start_polling()
        updater.idle()

    except Exception as e:
        logging.exception(f'Произошла ошибка в функции main: {e}')


if __name__ == '__main__':
    main()

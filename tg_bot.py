import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from environs import Env
from dialogflow import detect_intent_texts

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update):
    """Обработчик команды /start."""
    user = update.effective_user
    update.message.reply_markdown_v2(f'Здравствуйте {user.mention_markdown_v2()}')


def main():
    env = Env()
    env.read_env()
    project_id = env('PROJECT_ID')

    def handle_text(update):
        """Обработчик текстовых сообщений."""
        session_id = f'vk-{update.message.from_user.id}'
        text = update.message.text
        bot_response = detect_intent_texts(str(session_id), text, project_id)

        update.message.reply_text(bot_response)

    """Главная функция для запуска бота."""
    updater = Updater(env('TG_TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

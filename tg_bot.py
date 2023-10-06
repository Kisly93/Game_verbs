import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.cloud import dialogflow
from environs import Env


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


env = Env()
env.read_env()

project_id = env('PROJECT_ID')

def detect_intent_texts(session_id, text, language_code='ru-RU'):
    """Обработка текста через DialogFlow и возврат ответа."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={"session": session, "query_input": query_input})

    return response.query_result.fulfillment_text

def start(update, context):
    """Обработчик команды /start."""
    user = update.effective_user
    update.message.reply_markdown_v2(f'Здравствуйте {user.mention_markdown_v2()}!')

def help_command(update, context):
    """Обработчик команды /help."""
    update.message.reply_text('Help!')

def handle_text(update, context):
    """Обработчик текстовых сообщений."""
    user_id = update.message.from_user.id
    user_message = update.message.text
    bot_response = detect_intent_texts(str(user_id), user_message)

    update.message.reply_text(bot_response)

def main():
    """Главная функция для запуска бота."""
    updater = Updater(env('TG_TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

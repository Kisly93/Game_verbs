import logging

from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update, _):
    update.message.reply_text('Здравствуйте')

def help_command(update, _):
    update.message.reply_text('Help!')


def echo(update, _):
    update.message.reply_text(update.message.text)


def main():
    env = Env()
    env.read_env()
    updater = Updater(env('tg_token'))

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
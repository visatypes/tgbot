import logging
import os

from telegram.ext import Updater

from service.conversation.handler import conv_handler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info('Bot started')
    updater = Updater(os.environ['BOT_TOKEN'])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

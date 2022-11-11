import logging
import os
from typing import Any
from service.clients.api import client

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CHOOSING = 1
VISA_STATS = 2

JSON = dict[str, Any]


def start(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    question = """Привет.
Куда собрался?
    """
    assert update.message is not None
    assert context.user_data is not None

    countries = client.countries.get_all()
    context.user_data['countries'] = {country.name: country.uid for country in countries}
    reply_keyboard = [
        [country.name for country in countries],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=question, reply_markup=markup)

    return CHOOSING


def visa_choice(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    assert update.message is not None
    assert context.user_data is not None
    uid = context.user_data['countries'].get(update.message.text)
    if not uid:
        update.message.reply_text('Такой страны еще нет, но мы работаем над этим')
        return CHOOSING

    visas = client.countries.get_visas(uid)
    visa_names = {visa.name: visa.dict() for visa in visas}
    context.user_data['visas'] = visa_names

    choices = ', '.join(visa_names.keys())
    question = f'Какая виза интересует?\n {choices}'
    context.user_data['choice'] = 'visa'
    update.message.reply_text(question, reply_markup=ReplyKeyboardRemove())

    return VISA_STATS


def cancel(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    assert update.message is not None
    question = 'Досвидули'
    update.message.reply_text(question)

    return ConversationHandler.END


def visa_desc(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    assert update.message is not None
    assert context.user_data is not None
    visa = update.message.text
    info = context.user_data['visas'].get(visa)
    if not info:
        update.message.reply_text('Такой визы не существует')
        return VISA_STATS

    description = info['desc']
    answer = f'{visa}\n\n{description}'
    update.message.reply_text(answer)

    return ConversationHandler.END


def main():
    logger.info('Hello world')
    updater = Updater(os.environ['BOT_TOKEN'])
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.text, visa_choice,
                ),
            ],
            VISA_STATS: [
                MessageHandler(
                    Filters.text, visa_desc,
                ),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler

from service.clients.api import client
from service.conversation import states
from service.conversation.schemas import JSON


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

    return states.CHOOSING


def cancel(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    assert update.message is not None
    answer = 'Досвидули'
    update.message.reply_text(answer)

    return ConversationHandler.END

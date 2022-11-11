from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler

from service.clients.api import client
from service.conversation.schemas import JSON
from service.conversation.states import CHOOSING, VISA_STATS


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


def visa_desc(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    assert update.message is not None
    assert context.user_data is not None
    visa = update.message.text
    info_visa = context.user_data['visas'].get(visa)
    if not info_visa:
        update.message.reply_text('Такой визы не существует')
        return VISA_STATS

    description = info_visa['desc']
    answer = f'{visa}\n\n{description}'
    update.message.reply_text(answer)

    return ConversationHandler.END

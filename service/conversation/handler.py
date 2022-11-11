from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler

from service.conversation import states
from service.conversation.core import cancel, start
from service.conversation.visas import visa_choice, visa_desc

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        states.CHOOSING: [
            MessageHandler(
                Filters.text, visa_choice,
            ),
        ],
        states.VISA_STATS: [
            MessageHandler(
                Filters.text, visa_desc,
            ),
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

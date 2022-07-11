import json

from django.http import JsonResponse
from django.views import View

from django.conf import settings

from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

bot = Bot(token=settings.TELEGRAM_TOKEN)

def contact(update, context):
    chat = update.effective_chat
    phone = update.message.contact.phone_number

    bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо за предоставленные данные'
    )
    # request

def start(update, context):
    chat = update.effective_chat
    button = KeyboardButton('дай телефон плз', request_contact=True)

    bot.send_message(
        chat_id=chat.id,
        text='Привет?',
        reply_markup=ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    )


def setup_dispatch(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.contact, contact))

    return dispatcher

dispatcher = setup_dispatch(Dispatcher(bot, update_queue=None, use_context=True))


class telegramWebhookView(View):
    
    def post(self, request):
        update = Update.de_json(json.loads(request.body), bot)
        dispatcher.process_update(update)

        return JsonResponse(
            {
                'ok': 'data was sent'
            }
        )



# после получения телефона - типа спасибо и пока
# добавить кнопку завершения
# добавить базу для записи - username, chat_id, phone

# ответ по request
# деплой какой-никакой
import json

from django.conf import settings
from django.http import JsonResponse
from django.views import View

from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import requests


bot = Bot(token=settings.TELEGRAM_TOKEN)


def contact(update, context):
    chat = update.effective_chat
    phone = update.message.contact.phone_number
    username = update.message.chat.username
    if settings.DEBUG:
        phone = '79991234567'
        username = 'username'

    bot.send_message(
        chat_id=chat.id,
        text='Спасибо за предоставленные данные'
    )

    data = json.dumps({'phone': phone, 'username': username})
    url = 'https://s1-nova.ru/app/private_test_python/'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    requests.post(url, data=data, headers=headers)


def start(update, context):
    chat = update.effective_chat
    button = KeyboardButton(
        'Пришлите, пожалуйста, ваш телефон',
        request_contact=True
    )

    bot.send_message(
        chat_id=chat.id,
        text='Привет!',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[button]],
            resize_keyboard=True
        )
    )


def setup_dispatch(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.contact, contact))

    return dispatcher


dispatcher = setup_dispatch(Dispatcher(
    bot, update_queue=None, use_context=True
))


class telegramWebhookView(View):
    def post(self, request):
        update = Update.de_json(json.loads(request.body), bot)
        dispatcher.process_update(update)

        return JsonResponse(
            {
                'ok': 'data was sent'
            }
        )

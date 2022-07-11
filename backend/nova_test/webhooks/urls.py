from django.urls import path

from .views import telegramWebhookView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('telegram_bot/', csrf_exempt(telegramWebhookView.as_view()), name='telegram_webhook')
]
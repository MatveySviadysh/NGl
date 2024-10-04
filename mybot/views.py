# views.py
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import requests
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

def send_telegram_message(token, chat_id, text):
    """Отправляет сообщение в Telegram чат."""
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    return response.json()

class SendMessageView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        chat_id = '1311107393'  # Убедитесь, что это ваш правильный chat_id

        if 'message' in body and body['message'] == '/start':
            token = os.getenv('7330108104:AAGR35aQZ7b-1kHZxIYb-6fB3wICgOQmf00')  # Используйте переменные окружения
            response_message = "/start"  # Это сообщение для отправки
            send_telegram_message(token, chat_id, response_message)
            return JsonResponse({'status': 'success', 'message': response_message})

        return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

class ButtonPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mybot/button.html')  # Проверьте правильность пути

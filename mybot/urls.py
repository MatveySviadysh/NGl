# mybot/urls.py
from django.urls import path
from .views import SendMessageView, ButtonPageView

urlpatterns = [
    path('send-message/', SendMessageView.as_view(), name='send_message'),
    path('button/', ButtonPageView.as_view(), name='button_page'),  # Add this line for the button page
]

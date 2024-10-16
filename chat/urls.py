from django.urls import path, include
from .views import *

urlpatterns = [
    path('chat/<int:chatroom_id>/', chat_with_tutor, name='chat_with_tutor'),
    path('tutor/chats/', tutor_chat_list, name='tutor_chat_list'),
]
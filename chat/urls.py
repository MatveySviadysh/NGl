from django.urls import path, include
from django.views.generic import RedirectView
from .views import *

urlpatterns = [
    path('with/tutor/', chat_with_tutor, name='chat_with_tutor'),
]
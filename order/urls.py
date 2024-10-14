from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('answer/', answer, name='answer'),
]

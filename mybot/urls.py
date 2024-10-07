from django.urls import path
from .views import ButtonPageView

urlpatterns = [
    path('button/', ButtonPageView.as_view(), name='button_page'),
]

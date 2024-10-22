from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('answer/', answer, name='answer'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

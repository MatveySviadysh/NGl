from django.urls import path
from mybot import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('delete_all_messages/', views.delete_all_messages, name='delete_all_messages'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('button/', ButtonPageView.as_view(), name='button_page'),
    path('help-page/', Help_page, name='help-page'),
    path('my-messages/', UserMessagesView.as_view(), name='user_messages'),
    path('admin/support-message/<int:message_id>/', SupportMessageDetailView.as_view(), name='support_message_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

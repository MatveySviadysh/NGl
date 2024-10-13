from django.urls import path
from .views import ButtonPageView, UserMessagesView, SupportMessageDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('button/', ButtonPageView.as_view(), name='button_page'),
    path('my-messages/', UserMessagesView.as_view(), name='user_messages'),
    path('admin/support-message/<int:message_id>/', SupportMessageDetailView.as_view(), name='support_message_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

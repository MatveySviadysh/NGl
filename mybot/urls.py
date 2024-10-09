from django.urls import path
from .views import ButtonPageView, UserMessagesView, SupportMessageDetailView

urlpatterns = [
    path('button/', ButtonPageView.as_view(), name='button_page'),
    path('my-messages/', UserMessagesView.as_view(), name='user_messages'),
    path('admin/support-message/<int:message_id>/', SupportMessageDetailView.as_view(), name='support_message_detail'),

]

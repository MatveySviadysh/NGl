from django.urls import path
from .views import subscribe, unsubscribe, user_subscriptions

urlpatterns = [
    path('subscribe/<int:tutor_id>/', subscribe, name='subscribe'),
    path('unsubscribe/<int:tutor_id>/', unsubscribe, name='unsubscribe'),
    path('subscriptions/', user_subscriptions, name='user_subscriptions'), 
]

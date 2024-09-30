from django.urls import path
from .views import register, user_login, profile, user_logout

urlpatterns = [
    path('cabinet/user/register/', register, name='register-user'),
    path('cabinet/user/login/', user_login, name='login-user'),
    path('cabinet/user/logout/', user_logout, name='logout-user'),
    path('cabinet/user/', profile, name='profile-user'),
]

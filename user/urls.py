from django.urls import path
from .views import *

urlpatterns = [
    path('cabinet/user/register/', register, name='register-user'),
    path('cabinet/user/login/', user_login, name='login-user'),
    path('cabinet/user/logout/', user_logout, name='logout-user'),
    path('cabinet/user/', profile, name='profile-user'),
    path('main/', main_page, name='main-page'),
    path('cabinet/tutor/register/', register_tutor, name='register_tutor'),
    path('cabinet/tutor/login/', login_tutor, name='login_tutor'),
    path('cabinet/tutor/', profile_tutor, name='profile-tutor'),
    path('cabinet/tutor/logout/', tutor_logout, name='logout-tutor'), 
]


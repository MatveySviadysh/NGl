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
    path('tutors/<str:specialization>/', tutor_list, name='tutor_list'),
    path('all/tutors/', all_tutors, name='all_tutors'),
    path('cabinet/user/notifications/', notifications_user, name='notifications_user'),
    path('cabinet/user/change_password/', change_password_user, name='change-password-user'),
    path('tutors/', tutor_list_serarch, name='tutor-list-serarch'),
]


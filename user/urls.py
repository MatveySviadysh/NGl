from django.urls import path, include
from .views import *

urlpatterns = [
    path('cabinet/user/register/', register, name='register-user'),
    path('cabinet/user/login/', user_login, name='login-user'),
    path('cabinet/user/logout/', user_logout, name='logout-user'),
    path('cabinet/user/', profile_user, name='profile-user'),
    path('main/', main_page, name='main-page'),
    path('cabinet/tutor/register/', register_tutor, name='register_tutor'),
    path('cabinet/tutor/login/', login_tutor, name='login_tutor'),
    path('cabinet/tutor/<str:full_name>/', profile_tutor, name='profile-tutor'),
    path('cabinet/tutor/logout/', tutor_logout, name='logout-tutor'), 
    path('tutors/<str:specialization>/', tutor_list, name='tutor_list'),
    path('all/tutors/', all_tutors, name='all_tutors'),
    path('cabinet/user/change_password/', change_password_user, name='change-password-user'),
    path('tutors/', tutor_list_serarch, name='tutor-list-serarch'),
    path('user/reviews/create/', review_create, name='review_create'),
    path('user/chenge_user_profile/', chenge_user_profile, name='chenge_user_profile'),
    path('edit-profile/', edit_tutor_profile, name='edit-tutor-profile'),
    path('all_review/', all_review, name='all_review'),
    path('about_company/', about_company, name='about_company'),
    path('all_service/', all_service, name='all_service'),
    path('help/', help_page, name='help_page'),
    path('captcha/', include('captcha.urls')),
    path('foregin_password/',foregin_password,name = 'foregin_password')
]


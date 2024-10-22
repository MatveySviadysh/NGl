from django.urls import path
from . import views

urlpatterns = [
    path('tutor/<int:tutor_id>/comment/', views.add_comment, name='add_comment'),

]

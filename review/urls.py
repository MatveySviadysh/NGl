from django.urls import path
from . import views

urlpatterns = [
    path('tutor/<int:tutor_id>/comment/', views.add_comment, name='add_comment'),
    path('tutor_review/', views.ALLReviewTutor, name='all_review_tutor'),
]

from django.urls import path, include

urlpatterns = [
    path('order/', include('order.urls')),
]

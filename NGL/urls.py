from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/user/main/', permanent=False)), 
    path('user/', include('user.urls')),
    path('mybot/', include('mybot.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

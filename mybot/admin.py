from django.contrib import admin
from .models import SupportMessage

class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    ordering = ('-created_at',)

admin.site.register(SupportMessage, SupportMessageAdmin)

from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'tutor', 'created_at')
    search_fields = ('user__username', 'tutor__user__username')
    list_filter = ('created_at',)

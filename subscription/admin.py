from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'tutor', 'created_at')  # Поля, которые вы хотите видеть в админке
    search_fields = ('user__username', 'tutor__user__username')  # Поля для поиска
    list_filter = ('created_at',)  # Фильтры на боковой панели

from django.contrib import admin
from .models import UserConsultation

@admin.register(UserConsultation)
class UserConsultationAdmin(admin.ModelAdmin):
    list_display = ('target_audience', 'age', 'gender', 'consultation_count', 'meeting_format', 'price')
    search_fields = ('target_audience', 'comments')
    list_filter = ('gender', 'meeting_format')
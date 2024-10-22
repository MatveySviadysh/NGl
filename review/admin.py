from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'tutor', 'created_at', 'rating')
    search_fields = ('content',)
    list_filter = ('created_at', 'rating')
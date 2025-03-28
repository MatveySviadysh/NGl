from django.contrib import admin
from django.utils.html import format_html
from .models import SupportMessage

class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'image_tag')
    ordering = ('-created_at',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return '(No Image)'

    image_tag.short_description = 'Image'

admin.site.register(SupportMessage, SupportMessageAdmin)

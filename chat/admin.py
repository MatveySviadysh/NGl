from django.contrib import admin
from .models import ChatRoom, Message

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('requester', 'responder', 'chat_type', 'last_message', 'created_at', 'updated_at')
    search_fields = ('requester__username', 'responder__username', 'chat_type')
    list_filter = ('chat_type',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'chatroom', 'content', 'is_read', 'created_at')
    search_fields = ('sender__username', 'recipient__username', 'content')
    list_filter = ('is_read',)

admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message, MessageAdmin)

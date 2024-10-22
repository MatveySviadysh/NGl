from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    requester = models.ForeignKey(User, related_name='requester', on_delete=models.CASCADE)
    responder = models.ForeignKey(User, related_name='responder', on_delete=models.CASCADE)
    chat_type = models.CharField(max_length=50)
    last_message = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Chat between {self.requester.username} and {self.responder.username}'

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='messages_sent', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='messages_received', on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Message from {self.sender.username} to {self.recipient.username}'

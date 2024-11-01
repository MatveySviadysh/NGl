from django.db import models
from django.contrib.auth.models import User
from user.models import Tutor

class Comment(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.tutor.full_name}"
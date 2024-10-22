from django.db import models
from django.contrib.auth.models import User

from user.models import Tutor


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tutor')
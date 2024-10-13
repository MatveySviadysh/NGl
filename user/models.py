from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,User
from django.db import models
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

phone_validator = RegexValidator(
    regex=r'^\+375\d{9}$',
    message="Введите номер телефона в формате: +375xxxxxxxxx (9 цифр после +375)."
)

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=15,
        validators=[phone_validator]
    )
    specialization = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    tutor_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    verified = models.BooleanField(default=False)
    services = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    last_login = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.full_name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    username = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username}: {self.comment[:20]}... (Рейтинг: {self.rating})'
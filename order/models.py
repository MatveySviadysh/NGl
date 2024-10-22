from django.db import models

class UserConsultation(models.Model):
    TARGET_AUDIENCE_CHOICES = [
        ('для себя', 'Для себя'),
        ('для ребенка', 'Для ребенка'),
        ('для семьи', 'Для семьи'),
    ]

    GENDER_CHOICES = [
        ('мужчина', 'Мужчина'),
        ('женщина', 'Женщина'),
        ('не важно', 'Не важно'),
    ]

    consultation_count_choices = [
        ('1-2', '1-2'),
        ('решу позже', 'Решу после первой консультации'),
    ]

    MEETING_FORMAT_CHOICES = [
        ('онлайн', 'Онлайн'),
        ('лично', 'Лично'),
    ]

    target_audience = models.CharField(max_length=20, choices=TARGET_AUDIENCE_CHOICES)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    consultation_count = models.CharField(max_length=20, choices=consultation_count_choices)
    meeting_format = models.CharField(max_length=10, choices=MEETING_FORMAT_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    comments = models.TextField(blank=True)
    specialization = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.target_audience} - {self.age} лет"
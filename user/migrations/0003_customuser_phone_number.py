# Generated by Django 4.2.15 on 2024-10-01 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_customuser_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, help_text='Введите номер телефона', max_length=15, null=True),
        ),
    ]

# Generated by Django 4.2.15 on 2024-10-02 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_tutor_avatar_tutor_experience_tutor_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

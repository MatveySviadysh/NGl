# Generated by Django 4.2.15 on 2024-10-14 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_userconsultation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userconsultation',
            name='specialization',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
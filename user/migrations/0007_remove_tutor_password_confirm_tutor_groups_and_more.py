# Generated by Django 4.2.15 on 2024-10-02 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('user', '0006_tutor_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor',
            name='password_confirm',
        ),
        migrations.AddField(
            model_name='tutor',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='tutor_set', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='tutor',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='tutor',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='tutor_set', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]

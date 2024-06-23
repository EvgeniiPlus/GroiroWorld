# Generated by Django 4.1 on 2024-06-22 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='nophoto.jpg', null=True, upload_to=users.models.user_directory_path, verbose_name='Аватар')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='День рождения')),
                ('phone_number', models.CharField(blank=True, max_length=13, null=True, verbose_name='Номер телефона (моб.)')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
    ]

# Generated by Django 5.1 on 2024-08-27 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_profile_department_delete_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='telegram_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Telegram ID'),
        ),
    ]

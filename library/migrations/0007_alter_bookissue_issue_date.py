# Generated by Django 5.1 on 2024-08-21 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_alter_bookissue_reader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookissue',
            name='issue_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Выдано'),
        ),
    ]
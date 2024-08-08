# Generated by Django 4.1 on 2024-08-07 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='card_amount',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество (безналичные)'),
        ),
        migrations.AddField(
            model_name='reports',
            name='card_nds',
            field=models.FloatField(blank=True, default=0, verbose_name='Из них НДС (безналичные)'),
        ),
        migrations.AddField(
            model_name='reports',
            name='card_sum',
            field=models.FloatField(default=0, verbose_name='Сумма (безналичные)'),
        ),
        migrations.AddField(
            model_name='reports',
            name='cash_amount',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество (наличные)'),
        ),
        migrations.AddField(
            model_name='reports',
            name='cash_nds',
            field=models.FloatField(blank=True, default=0, verbose_name='Из них НДС (наличные)'),
        ),
        migrations.AddField(
            model_name='reports',
            name='cash_sum',
            field=models.FloatField(default=0, verbose_name='Сумма (наличные)'),
        ),
        migrations.AlterField(
            model_name='reports',
            name='amount',
            field=models.PositiveIntegerField(verbose_name='Количество (общее)'),
        ),
        migrations.AlterField(
            model_name='reports',
            name='nds',
            field=models.FloatField(blank=True, default=0, verbose_name='Из них НДС (общее)'),
        ),
        migrations.AlterField(
            model_name='reports',
            name='sum',
            field=models.FloatField(verbose_name='Сумма (общее)'),
        ),
    ]

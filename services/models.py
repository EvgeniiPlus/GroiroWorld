from users.models import *
from django.db import models



def user_directory_path(instance, filename):
    return 'user_{0}/avatars/{1}'.format(instance.user.id, filename)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен", null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Structures(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    employee = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Сотрудник")
    plan = models.FloatField(default=0, verbose_name='План')
    earned = models.FloatField(default=0, verbose_name='Заработано')

    class Meta:
        verbose_name = 'Структура'
        verbose_name_plural = 'Структуры'

    def __str__(self):
        return self.name


class Services(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    structure = models.ForeignKey('Structures', on_delete=models.PROTECT, verbose_name="Структура")
    price = models.FloatField(verbose_name="Стоимость")

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


class Reports(models.Model):
    date = models.DateField(verbose_name='Дата')
    structure = models.ForeignKey('Structures', on_delete=models.PROTECT, verbose_name="Структура")
    service = models.ForeignKey('Services', on_delete=models.SET_NULL, null=True, verbose_name="Услуга")

    # Наличный рассчет
    cash_amount = models.PositiveIntegerField(verbose_name="Количество (наличные)", default=0)
    cash_sum = models.FloatField(verbose_name="Сумма (наличные)", default=0)
    cash_nds = models.FloatField(verbose_name='Из них НДС (наличные)', blank=True, default=0)

    #Безналичный рассчет
    card_amount = models.PositiveIntegerField(verbose_name="Количество (безналичные)", default=0)
    card_sum = models.FloatField(verbose_name="Сумма (безналичные)", default=0)
    card_nds = models.FloatField(verbose_name='Из них НДС (безналичные)', blank=True, default=0)

    #Общая
    amount = models.PositiveIntegerField(verbose_name="Количество (общее)")
    sum = models.FloatField(verbose_name="Сумма (общее)")
    nds = models.FloatField(verbose_name='Из них НДС (общее)', blank=True, default=0)

    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    date_edit = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'

    def __str__(self):
        return f'{self.date} {self.service}'

#
# class Orders(models.Model):
#     service = models.ForeignKey('Services', on_delete=models.PROTECT, verbose_name='Услуга')
#     client_name = models.CharField(max_length=200, verbose_name='Имя клиента')
#     sum = models.FloatField(verbose_name='Сумма заказа')
#     email = models.EmailField(verbose_name='E-mail клиента', blank=True)
#     phone = models.CharField(max_length=15, verbose_name='Телефон клиента')
#     date_of_receiving = models.DateTimeField(verbose_name='Желаемая дата получения заказа', blank=True)
#     comment = models.TextField(verbose_name='Комментарий к заказу', blank=True)
#     file = models.FileField(upload_to='uploads/ordersIBC/%Y/%m/%d/', verbose_name='Файл')
#     status = models.CharField(max_length=15, verbose_name='Статус заказа')
#     date_create = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
#     date_edit = models.DateTimeField(auto_now=True, verbose_name="Изменено")
#
#     class Meta:
#         verbose_name = 'Заказ'
#         verbose_name_plural = 'Заказы'
#
#     def __str__(self):
#         return f'{self.client_name} {self.service}'

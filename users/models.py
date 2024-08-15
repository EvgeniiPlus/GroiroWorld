from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return 'users/user_{0}/avatars/{1}'.format(instance.user.id, filename)


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    short_name = models.CharField(max_length=50, verbose_name="Аббревиатура")

    class Meta:
        verbose_name = 'Структурное подразделение'
        verbose_name_plural = 'Структурные подразделения'

    def __str__(self):
        return f'{self.name}'


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(upload_to=user_directory_path, default='nophoto.jpg', null=True, verbose_name="Аватар")
    birthday = models.DateField(verbose_name="День рождения", null=True, blank=True)
    phone_number = models.CharField(max_length=13, verbose_name="Номер телефона (моб.)", null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name="Структурное подразделение")

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'{self.user}'

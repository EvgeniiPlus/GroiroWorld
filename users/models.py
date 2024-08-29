from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return 'users/user_{0}/avatars/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(upload_to=user_directory_path, default='nophoto.jpg', null=True, verbose_name="Аватар")
    birthday = models.DateField(verbose_name="День рождения", null=True, blank=True)
    phone_number = models.CharField(max_length=13, verbose_name="Номер телефона (моб.)", null=True, blank=True)
    telegram_id = models.IntegerField(verbose_name="Telegram ID", null=True, blank=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'{self.user}'

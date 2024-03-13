# from django.db import models
# from django.contrib.auth.models import User
#
#
# def user_directory_path(instance, filename):
#     return 'users/user_{0}/avatars/{1}'.format(instance.user.id, filename)
#
#
# class Users(models.Model):
#     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
#     surname = models.CharField(max_length=100, verbose_name="Фамилия")
#     name = models.CharField(max_length=150, verbose_name="Имя, отчество")
#     role = models.ForeignKey('Roles', on_delete=models.PROTECT, verbose_name='Роль')
#     email = models.EmailField(max_length=200, unique=True, verbose_name="email")
#     avatar = models.ImageField(upload_to=user_directory_path, default='nophoto.jpg', null=True, verbose_name="Аватар")
#
#     class Meta:
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'
#
#     def __str__(self):
#         return f'{self.surname} {self.name}'
#
#
# class Roles(models.Model):
#     name = models.CharField(max_length=100, verbose_name="Название")
#     description = models.TextField(blank=True, verbose_name="Описание")
#
#     class Meta:
#         verbose_name = 'Роль'
#         verbose_name_plural = 'Роли'
#
#     def __str__(self):
#         return self.name

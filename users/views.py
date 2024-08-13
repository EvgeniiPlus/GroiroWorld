from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .models import *

menu = [{'title': 'Главная', 'url_name': 'home', 'icon': 'fas fa-home fa-sm fa-fw me-2 text-gray-400',
         'role': ['Администраторы', 'Операторы', 'Экономисты']},
        {'title': 'Создать отчет', 'url_name': 'dailyReport',
         'icon': 'fas fa-plus-square fa-sm fa-fw me-2 text-gray-400', 'role': ['Операторы']},
        {'title': 'Мои отчеты', 'url_name': 'myReports', 'icon': 'fas fa-file fa-sm fa-fw me-2 text-gray-400',
         'role': ['Операторы']},
        {'title': 'Мои услуги', 'url_name': 'myServices', 'icon': 'fas fa-tasks fa-sm fa-fw me-2 text-gray-400',
         'role': ['Операторы']},
        {'title': 'Отчеты', 'url_name': 'chooseStructure', 'icon': 'fas fa-file fa-sm fa-fw me-2 text-gray-400',
         'role': ['Администраторы', 'Экономисты']},
        {'title': 'Заказать услугу ИБЦ', 'url_name': 'ibc', 'icon': 'fas fa-print fa-sm fa-fw me-2 text-gray-400',
         'role': ['Пользователи']},
        ]

userMenu = [{'title': 'Профиль', 'url_name': 'profile', 'icon': 'fas fa-user fa-sm fa-fw me-2 text-gray-400',
             'role': ['Администраторы', 'Операторы', 'Экономисты']},
            {'title': 'Админ-панель', 'url_name': 'admin:index', 'icon': 'fas fa-cogs fa-sm fa-fw me-2 text-gray-400',
             'role': ['Администраторы']},
            {'title': 'Выйти', 'url_name': 'logout', 'icon': 'fas fa-sign-out-alt fa-sm fa-fw me-2 text-gray-400',
             'role': ['Администраторы', 'Операторы', 'Экономисты']},
            ]


@login_required
def profile(request):
    user = auth.get_user(request)
    group = request.user.groups.values_list('name', flat=True).first()
    userInfo = User.objects.get(username=user)
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Мой профиль',
        'userInfo': userInfo,
        'userAvatar': Profile.objects.get(user=user).avatar,
        'userRole': str(group),
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        surname = request.POST.get('surname')

        try:
            updUser = User.objects.get(username=user)
            updUser.last_name = surname
            updUser.first_name = name
            updUser.email = email

            updUser.save(update_fields=['last_name', 'first_name', 'email'])

            if request.FILES:
                upd_avatar = Profile.objects.get(user=user)
                upd_avatar.avatar = request.FILES['avatar']
                upd_avatar.save(update_fields=['avatar'])

            # print(f'+++++++++++++++++++++Update user "{updUser.username}" success!')

        except Exception as e:
            print(e)

        return redirect('profile')

    return render(request, 'profile.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')

# from django.shortcuts import render, redirect
#
# from .models import *
#
# menu = [{'title': 'Главная', 'url_name': 'home', 'icon': 'fas fa-home fa-sm fa-fw me-2 text-gray-400',
#          'role': ['Администратор', 'Оператор', 'Экономист']},
#         {'title': 'Создать отчет', 'url_name': 'dailyReport',
#          'icon': 'fas fa-plus-square fa-sm fa-fw me-2 text-gray-400', 'role': ['Оператор']},
#         {'title': 'Мои отчеты', 'url_name': 'myReports', 'icon': 'fas fa-file fa-sm fa-fw me-2 text-gray-400',
#          'role': ['Оператор']},
#         {'title': 'Мои услуги', 'url_name': 'myServices', 'icon': 'fas fa-tasks fa-sm fa-fw me-2 text-gray-400',
#          'role': ['Оператор']},
#         {'title': 'Отчеты', 'url_name': 'chooseStructure', 'icon': 'fas fa-file fa-sm fa-fw me-2 text-gray-400',
#          'role': ['Администратор', 'Экономист']},
#         {'title': 'Заказать услугу ИБЦ', 'url_name': 'ibc', 'icon': 'fas fa-print fa-sm fa-fw me-2 text-gray-400',
#          'role': ['Пользователь']},
#         ]
#
# userMenu = [{'title': 'Профиль', 'url_name': 'profile', 'icon': 'fas fa-user fa-sm fa-fw me-2 text-gray-400',
#              'role': ['Администратор', 'Оператор', 'Экономист']},
#             {'title': 'Админ-панель', 'url_name': 'admin:index', 'icon': 'fas fa-cogs fa-sm fa-fw me-2 text-gray-400',
#              'role': ['Администратор']},
#             {'title': 'Выйти', 'url_name': 'logout', 'icon': 'fas fa-sign-out-alt fa-sm fa-fw me-2 text-gray-400',
#              'role': ['Администратор', 'Оператор', 'Экономист']},
#             ]
#
# def profile(request):
#     userInfo = Users.objects.get(user=request.user)
#     context = {
#         'menu': menu,
#         'userMenu': userMenu,
#         'title': 'Мой профиль',
#         'userInfo': userInfo,
#         'userAvatar': userInfo.avatar,
#         'userRole': str(Users.objects.get(user=request.user).role),
#     }
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         name = request.POST.get('name')
#         surname = request.POST.get('surname')
#
#         try:
#             updUser = Users.objects.get(user=request.user)
#             updUser.surname = surname
#             updUser.name = name
#             updUser.email = email
#             if request.FILES:
#                 updUser.avatar = request.FILES['avatar']
#             else:
#                 updUser.avatar = userInfo.avatar
#             updUser.save(update_fields=['name', 'email', 'avatar', 'surname'])
#
#             print(f'+++++++++++++++++++++Update user "{updUser.user}" success!')
#
#         except Exception as e:
#             print(e)
#
#         return redirect('profile')
#
#     return render(request, 'new_services/profile.html', context)

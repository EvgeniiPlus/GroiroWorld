import datetime
import mimetypes
import os
from time import strftime
from wsgiref.util import FileWrapper

from _ctypes import Structure
from django.utils import timezone
from pytils import translit
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import *
from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView

import pandas
# from pypdf import PdfFileReader, PdfReader
import locale
from docxtpl import DocxTemplate
from num2t4ru import decimal2text
# import aspose.words as aw

# Create your views here.

menu = [{'title': 'Главная', 'url_name': 'home', 'icon': 'fas fa-home fa-sm fa-fw me-2 text-gray-400',
         'role': ['Администратор', 'Оператор', 'Экономист']},
        {'title': 'Создать отчет', 'url_name': 'dailyReport',
         'icon': 'fas fa-plus-square fa-sm fa-fw me-2 text-gray-400', 'role': ['Оператор']},
        {'title': 'Мои отчеты', 'url_name': 'myReports', 'icon': 'fas fa-file fa-sm fa-fw me-2 text-gray-400',
         'role': ['Оператор']},
        {'title': 'Мои услуги', 'url_name': 'myServices', 'icon': 'fas fa-tasks fa-sm fa-fw me-2 text-gray-400',
         'role': ['Оператор']},
        {'title': 'Отчеты', 'url_name': 'chooseStructure', 'icon': 'fas fa-file fa-sm fa-fw me-2 text-gray-400',
         'role': ['Администратор', 'Экономист']},
        {'title': 'Заказать услугу ИБЦ', 'url_name': 'ibc', 'icon': 'fas fa-print fa-sm fa-fw me-2 text-gray-400',
         'role': ['Пользователь']},
        ]

userMenu = [{'title': 'Профиль', 'url_name': 'profile', 'icon': 'fas fa-user fa-sm fa-fw me-2 text-gray-400',
             'role': ['Администратор', 'Оператор', 'Экономист']},
            {'title': 'Админ-панель', 'url_name': 'admin:index', 'icon': 'fas fa-cogs fa-sm fa-fw me-2 text-gray-400',
             'role': ['Администратор']},
            {'title': 'Выйти', 'url_name': 'logout', 'icon': 'fas fa-sign-out-alt fa-sm fa-fw me-2 text-gray-400',
             'role': ['Администратор', 'Оператор', 'Экономист']},
            ]


@login_required
def home(request):
    locale.setlocale(locale.LC_TIME, 'ru')
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'ГрОИРО. Услуги',
        'userAvatar': Users.objects.get(user=request.user).avatar,
    }

    if str(Users.objects.get(user=request.user).role) == 'Оператор':
        context['structure'] = Structures.objects.get(employee=Users.objects.get(user=request.user))
        reports = Reports.objects.filter(structure=context['structure'],
                                         date__gte=f"{timezone.now().year}-01-01").order_by('date')
        services = Services.objects.filter(
            structure=Structures.objects.get(employee=Users.objects.get(user=request.user)))

        # График
        chart = {}
        for report in reports:
            if report.date.strftime("%B") not in chart:
                chart[report.date.strftime("%B")] = report.sum
            else:
                sum = chart[report.date.strftime("%B")]
                chart[report.date.strftime("%B")] = sum + report.sum
        context['chart'] = chart

        # Подсчет количества оказанных в текущем году услуг
        services_sum = {}
        for service in services:
            reports = Reports.objects.filter(service=service, date__gte=f"{timezone.now().year}-01-01")
            sum = 0
            for report in reports:
                sum += report.sum
            services_sum[service.name] = round(sum, 2)
        context['services_sum'] = services_sum

        context['main_progress'] = round(context['structure'].earned / context['structure'].plan * 100, 1)

    elif (str(Users.objects.get(user=request.user).role) == 'Экономист' or
          str(Users.objects.get(user=request.user).role) == 'Администратор'):

        reports = Reports.objects.filter(date__gte=f"{timezone.now().year}-01-01").order_by('date')
        structures = Structures.objects.all()
        # Заработано средств
        sum = 0
        plan = 0
        for structure in structures:
            sum += structure.earned
            plan += structure.plan
        context['earned'] = round(sum, 2)
        context['plan'] = round(plan, 2)

        # Выполнение плана
        context['main_progress'] = round(sum / plan * 100, 1)

        # График
        chart = {}
        for report in reports:
            if report.date.strftime("%B") not in chart:
                chart[report.date.strftime("%B")] = round(report.sum, 2)
            else:
                sum = chart[report.date.strftime("%B")]
                chart[report.date.strftime("%B")] = round(sum + report.sum, 2)
        context['chart'] = chart

        # Выполнение по каждой услуге
        services_sum = {}
        for service in Services.objects.all():
            reports = Reports.objects.filter(service=service, date__gte=f"{timezone.now().year}-01-01")
            sum = 0
            for report in reports:
                sum += report.sum
            services_sum[service.name] = round(sum, 2)
        context['services_sum'] = services_sum

    if request.user.is_authenticated:
        context['userRole'] = str(Users.objects.get(user=request.user).role)

    if request.method == 'POST':
        operator_name = str(Users.objects.get(user=request.user).name)
        operator_surname = str(Users.objects.get(user=request.user).surname)
        IOF_operator = operator_name.split(' ')[0][0] + '.' + operator_name.split(' ')[1][0] + '.' + operator_surname
        FIO_operator = operator_surname + ' ' + operator_name.split(' ')[0][0] + '.' + operator_name.split(' ')[1][0] + '.'


        date = request.POST.get('date').split('-')[2] + '.' + request.POST.get('date').split('-')[1] + '.' + request.POST.get('date').split('-')[0]

        reports_to_print = Reports.objects.filter(structure=Structures.objects.get(employee=Users.objects.get(user=request.user)), date=request.POST.get('date'))
        int_units = ((u'рубль', u'рубля', u'рублей'), 'm')
        exp_units = ((u'копейка', u'копейки', u'копеек'), 'f')
        sum = 0
        nds = 0
        servs = ''
        for i, r in enumerate(reports_to_print):
            sum += r.sum
            nds += r.nds
            servs += f'\t{i+1}. {r.service.name} {(str(r.sum).split(".")[0])} руб. {str("{:.2f}".format(r.sum)).split(".")[1]} коп. ({decimal2text(r.sum,int_units=int_units, exp_units=exp_units)}), ' \
                     f'в т.ч. НДС - {str(r.nds).split(".")[0]} руб. {str("{:.2f}".format(r.nds)).split(".")[1]} коп.({decimal2text(r.nds,int_units=int_units, exp_units=exp_units)}).\n'

        data = {'res': f'Всего: {str(sum).split(".")[0]} руб. {str(sum).split(".")[1]} коп. ({decimal2text(sum, int_units=int_units, exp_units=exp_units)}), '
                       f'в т.ч. НДС – {str(nds).split(".")[0]} руб. {str(nds).split(".")[1]} коп.  ({decimal2text(nds, int_units=int_units, exp_units=exp_units)}).',
                'date': date,
                'IOF_operator': IOF_operator,
                'FIO_operator': FIO_operator,
                'servs': servs,
                }

        doc = DocxTemplate("services/static/template.docx")

        filename = f"Отчет {data['date']}.docx"
        filepath = f'services/reports/{filename}'
        doc.render(data)
        doc.save(filepath)

        chunk_size = 8192

        response = StreamingHttpResponse(FileResponse(open(filepath, 'rb'), chunk_size),
                                         content_type=mimetypes.guess_type(filepath)[0])

        response['Content-Length'] = os.path.getsize(filepath)
        response['Content-Disposition'] = "attachment; filename=%s" % filename

        return response
        # return redirect('home')

    return render(request, 'new_services/index.html', context)


def update_earned(request):
    sum = 0
    reports = Reports.objects.filter(structure=Structures.objects.get(employee=Users.objects.get(user=request.user)),
                                     date__gte=f"{timezone.now().year}-01-01")
    for report in reports:
        sum += report.sum
    updSum = Structures.objects.get(employee=Users.objects.get(user=request.user))
    updSum.earned = sum
    updSum.save(update_fields=['earned'])
    return redirect(home)


@login_required
def profile(request):
    userInfo = Users.objects.get(user=request.user)
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Мой профиль',
        'userInfo': userInfo,
        'userAvatar': userInfo.avatar,
        'userRole': str(Users.objects.get(user=request.user).role),
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        surname = request.POST.get('surname')

        try:
            updUser = Users.objects.get(user=request.user)
            updUser.surname = surname
            updUser.name = name
            updUser.email = email
            if request.FILES:
                updUser.avatar = request.FILES['avatar']
            else:
                updUser.avatar = userInfo.avatar
            updUser.save(update_fields=['name', 'email', 'avatar', 'surname'])

            print(f'+++++++++++++++++++++Update user "{updUser.user}" success!')

        except Exception as e:
            print(e)

        return redirect('profile')

    return render(request, 'new_services/profile.html', context)


@login_required
def dailyReport(request):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Ежедневный отчет',
        'services': Services.objects.filter(
            structure=Structures.objects.get(employee=Users.objects.get(user=request.user))),
        'structure': Structures.objects.filter(employee=Users.objects.get(user=request.user))[0],
        'current_date': timezone.now(),
        'userRole': str(Users.objects.get(user=request.user).role),
        'userAvatar': Users.objects.get(user=request.user).avatar,
    }

    if request.method == 'POST':
        date = request.POST.get('service_date')
        service_id_list = request.POST.getlist('service_id')
        service_count_list = request.POST.getlist('service_count')
        # print(f'{date} \n{service_id_list} \n{service_count_list}')

        for i in range(len(service_id_list)):
            sum = round(int(service_count_list[i]) * Services.objects.filter(pk=service_id_list[i])[0].price, 2)
            if int(service_count_list[i]) != 0:
                Reports.objects.create(
                    date=date,
                    service=Services.objects.get(pk=service_id_list[i]),
                    structure=Structures.objects.filter(employee=Users.objects.get(user=request.user))[0],
                    amount=service_count_list[i],
                    sum=sum,
                    nds=round(sum / 6, 2)
                )
                updSum = Structures.objects.get(employee=Users.objects.get(user=request.user))
                updSum.earned += sum
                updSum.save(update_fields=['earned'])
            else:
                continue

        return redirect('home')

    return render(request, 'new_services/DailyReport.html', context)


@login_required
def chooseStructure(request):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Выбор структуры',
        'structures': Structures.objects.all(),
        'userRole': str(Users.objects.get(user=request.user).role),
        'userAvatar': Users.objects.get(user=request.user).avatar,
    }

    return render(request, 'new_services/chooseStructure.html', context)


@login_required
def listReports(request, pk):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Отчеты',
        'structure': Structures.objects.filter(pk=pk).first,
        'services': Services.objects.filter(structure=Structures.objects.get(pk=pk)),
        'userRole': str(Users.objects.get(user=request.user).role),
        'reports': Reports.objects.filter(structure=pk, date__gte=f"{timezone.now().year}-01-01").order_by('-date'),
        'userAvatar': Users.objects.get(user=request.user).avatar,
    }

    if request.method == 'POST':
        date_start = str(request.POST.get('date_start'))
        date_finish = str(request.POST.get('date_finish'))
        service = request.POST.get('service')
        print(f'c _{date_start}_ po _{date_finish}_')

        if date_start and date_finish != '' and service != 'all':
            print(date_start, date_finish, service)
            context['reports'] = Reports.objects.filter(structure=pk, service=Services.objects.get(pk=service),
                                                        date__gte=date_start,
                                                        date__lte=date_finish).order_by('-date')
            context['date_start'] = date_start
            context['date_finish'] = date_finish
            context['service'] = Services.objects.get(pk=service)


        elif date_start != '' and date_finish != '' and service == 'all':
            print(date_start, date_finish, service)
            context['reports'] = Reports.objects.filter(structure=pk, date__gte=date_start,
                                                        date__lte=date_finish).order_by('-date')
            context['date_start'] = date_start
            context['date_finish'] = date_finish

        elif date_start == '' and date_finish == '' and service != 'all':
            print(service)
            context['reports'] = Reports.objects.filter(structure=pk, service=service).order_by('-date')
            context['service'] = Services.objects.get(pk=service)

        else:
            print('date_start', 'date_finish', service)
            context['reports'] = Reports.objects.filter(structure=pk).order_by('-date')

    return render(request, 'new_services/listReports.html', context)


def downloadReport(request):
    service = request.GET.get('service')
    date_start = request.GET.get('date_start')
    date_finish = request.GET.get('date_finish')
    structure = request.GET.get('structure')

    if str(Users.objects.get(user=request.user).role) == 'Оператор':
        pk = Structures.objects.get(employee=Users.objects.get(user=request.user)).pk
        reports = Reports.objects.filter(structure=Structures.objects.get(pk=pk))
    elif (str(Users.objects.get(user=request.user).role) == 'Экономист' or
          str(Users.objects.get(user=request.user).role) == 'Администратор'):
        reports = Reports.objects.filter(structure=Structures.objects.get(name=structure))

    if date_start and date_finish != '' and service != 'all':

        reports = reports.filter(service=Services.objects.get(pk=service),
                                 date__gte=date_start,
                                 date__lte=date_finish)

    elif date_start and date_finish != '' and service == 'all':

        reports = reports.filter(
            date__gte=date_start,
            date__lte=date_finish)

    elif date_start and date_finish == '' and service != 'all':

        reports = reports.filter(
            service=Services.objects.get(pk=service))

    else:
        reports = reports

    dates = []
    services = []
    amounts = []
    sums = []

    for r in reports:
        dates.append(r.date)
        services.append(r.service)
        amounts.append(r.amount)
        sums.append(r.sum)

    dates.append('')
    sums.append(f'=SUM(D2:D{len(sums) + 1})')
    amounts.append(f'=SUM(C2:C{len(amounts) + 1})')
    services.append('Итого:')

    df = pandas.DataFrame({'Дата': dates,
                           'Услуга': services,
                           'Количество': amounts,
                           'Сумма': sums,
                           })
    if date_start and date_finish == '':
        filename = f'Отчет_all_time.xlsx'
    else:
        filename = f'Отчет_{date_start}-{date_finish}.xlsx'

    filepath = f'services/reports/{filename}'
    df.to_excel(filepath, index=False)

    chunk_size = 8192

    response = StreamingHttpResponse(FileResponse(open(filepath, 'rb'), chunk_size),
                                     content_type=mimetypes.guess_type(filepath)[0])

    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response


@login_required
def myReports(request):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Мои отчеты',
        'services': Services.objects.filter(
            structure=Structures.objects.get(employee=Users.objects.get(user=request.user))),
        'structure': Structures.objects.filter(employee=Users.objects.get(user=request.user)).first,
        'userRole': str(Users.objects.get(user=request.user).role),
        'reports': Reports.objects.filter(
            structure=Structures.objects.get(employee=Users.objects.get(user=request.user)),
            date__gte=f"{timezone.now().year}-01-01").order_by('-date'),
        'userAvatar': Users.objects.get(user=request.user).avatar,
    }
    if request.method == 'POST':
        pk = Structures.objects.get(employee=Users.objects.get(user=request.user))
        date_start = str(request.POST.get('date_start'))
        date_finish = str(request.POST.get('date_finish'))
        service = request.POST.get('service')

        if date_start and date_finish != '' and service != 'all':
            context['reports'] = Reports.objects.filter(structure=pk, service=Services.objects.get(pk=service),
                                                        date__gte=date_start,
                                                        date__lte=date_finish).order_by('-date')
            context['date_start'] = date_start
            context['date_finish'] = date_finish
            context['service'] = Services.objects.get(pk=service)


        elif date_start != '' and date_finish != '' and service == 'all':
            print(date_start, date_finish, service)
            context['reports'] = Reports.objects.filter(structure=pk, date__gte=date_start,
                                                        date__lte=date_finish).order_by('-date')
            context['date_start'] = date_start
            context['date_finish'] = date_finish

        elif date_start == '' and date_finish == '' and service != 'all':
            print(service)
            context['reports'] = Reports.objects.filter(structure=pk, service=service).order_by('-date')
            context['service'] = Services.objects.get(pk=service)

        else:
            print('date_start', 'date_finish', service)
            context['reports'] = Reports.objects.filter(structure=pk).order_by('-date')

    return render(request, 'new_services/listReports.html', context)


@login_required
def myServices(request):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Мои услуги',
        'userRole': str(Users.objects.get(user=request.user).role),
        'services': Services.objects.filter(
            structure=Structures.objects.get(employee=Users.objects.get(user=request.user))),
        # 'structure': Structures.objects.filter(employee=Users.objects.get(user=request.user)).first,
        'userAvatar': Users.objects.get(user=request.user).avatar,
    }

    if request.method == 'POST':
        pks = request.POST.getlist('pk')
        names = request.POST.getlist('name')
        descriptions = request.POST.getlist('description')
        prices = request.POST.getlist('price')

        # Services.objects.bulk_update(
        #     [names[i]] for i in range(len(names)),
        #
        # )
        for i in range(len(names)):
            Services.objects.filter(pk=pks[i]).update(name=names[i], description=descriptions[i], price=prices[i])

        return redirect('myServices')

    return render(request, 'new_services/my_services.html', context)


def del_service(request, pk):
    Services.objects.get_or_404(pk=pk).delete()
    return redirect(myServices)


@login_required
def newService(request):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Новая услуга',
        'userRole': str(Users.objects.get(user=request.user).role),
        'structure': Structures.objects.filter(employee=Users.objects.get(user=request.user)).first,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        Services.objects.create(name=name, description=description, price=price,
                                structure=Structures.objects.filter(employee=Users.objects.get(user=request.user))[0])
        return redirect('myServices')

    return render(request, 'new_services/newService.html', context)


@login_required
def ibcNewOrder(request):
    price = Services.objects.get(name='Печать').price
    context = {
        'title': 'Новый заказ',
        'price': price
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_of_receiving = request.POST.get('date_of_receiving')
        document = str(request.FILES['document']).replace(' ', '_')
        comment = request.POST.get('comment')
        #
        # count_pages = len(PdfReader(document).pages)
        # print(f'{count_pages} страниц')

        order = Orders(service=Services.objects.get(pk=1),
                       client_name=name,
                       sum=0,
                       email=email,
                       phone=phone,
                       date_of_receiving=date_of_receiving,
                       comment=comment,
                       file=request.FILES['document'],
                       status='Заказ принят')
        order.save()
        print('save ok ----> ', document)
        # doc = aw.Document(f'./uploads/ordersIBC/{strftime("%Y")}/{strftime("%m")}/{strftime("%d")}/{document}')
        # Orders.objects.filter(pk=order.id).update(sum=price * doc.page_count)
        # print('update ok ---> ', document)

    return render(request, 'new_services/ibcNewOrder.html', context)

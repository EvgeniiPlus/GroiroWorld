import datetime
import mimetypes
import os
from time import strftime
from wsgiref.util import FileWrapper

from _ctypes import Structure
from django.contrib import auth
from django.utils import timezone
from pytils import translit
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import *
from users.models import *
from django.contrib.auth.models import User

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

main_menu = [{'title': 'Главная', 'url_name': 'home', 'icon': 'fas fa-home fa-sm fa-fw me-2 text-gray-400',
              'role': ['Администраторы', 'Операторы', 'Экономисты']},
             {'title': 'Создать отчет', 'url_name': 'dailyReport',
              'icon': 'fas fa-plus-square fa-sm fa-fw me-2 text-gray-400', 'role': ['Операторы']},
             {'title': 'Мои отчеты', 'url_name': 'myReports', 'icon': 'fas fa-file fa-sm fa-fw me-2 text-gray-400',
              'role': ['Операторы']},
             {'title': 'Мои услуги', 'url_name': 'myServices', 'icon': 'fas fa-tasks fa-sm fa-fw me-2 text-gray-400',
              'role': ['Операторы']},
             {'title': 'Отчеты', 'url_name': 'chooseStructure', 'icon': 'fas fa-file fa-sm fa-fw me-2 text-gray-400',
              'role': ['Администраторы', 'Экономисты']},
             ]

user_menu = [{'title': 'Профиль', 'url_name': 'profile', 'icon': 'fas fa-user fa-sm fa-fw me-2 text-gray-400',
              'role': ['Администраторы', 'Операторы', 'Экономисты']},
             {'title': 'Админ-панель', 'url_name': 'admin:index', 'icon': 'fas fa-cogs fa-sm fa-fw me-2 text-gray-400',
              'role': ['Администраторы']},
             {'title': 'Выйти', 'url_name': 'logout', 'icon': 'fas fa-sign-out-alt fa-sm fa-fw me-2 text-gray-400',
              'role': ['Администраторы', 'Операторы', 'Экономисты']}
             ]


def get_menu(groups):
    menu = []
    for group in groups:
        for menu_item in main_menu:
            if group in menu_item['role']:
                menu.append(menu_item)
    return menu


def get_user_menu(groups):
    menu = []
    for group in groups:
        for menu_item in user_menu:
            if group in menu_item['role']:
                menu.append(menu_item)
    return menu


@login_required
def home(request):
    # locale.setlocale(locale.LC_TIME, 'ru')
    user = auth.get_user(request)
    groups = request.user.groups.values_list('name', flat=True)
    context = {
        'menu': get_menu(groups),
        'user_menu': get_user_menu(groups),
        'title': 'ГрОИРО. Услуги',
        'userAvatar': Profile.objects.get(user=request.user).avatar,
    }

    if 'Операторы' in groups:
        context['structure'] = Structures.objects.get(employee=user)
        reports = Reports.objects.filter(structure=context['structure'],
                                         date__gte=f"{timezone.now().year}-01-01").order_by('date')
        services = Services.objects.filter(
            structure=Structures.objects.get(employee=user))

        # График
        chart = {}
        for report in reports:
            if report.date.strftime("%B") not in chart:
                chart[report.date.strftime("%B")] = round(report.sum, 2)
            else:
                sum = chart[report.date.strftime("%B")]
                chart[report.date.strftime("%B")] = round(sum + report.sum, 2)
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

    elif ('Экономисты' in groups or 'Администраторы' in groups):

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

    # if request.user.is_authenticated:
    #     context['userRole'] = group

    if request.method == 'POST':
        operator_name = str(user.first_name)
        operator_surname = str(user.last_name)
        IOF_operator = operator_name.split(' ')[0][0] + '.' + operator_name.split(' ')[1][0] + '.' + operator_surname
        FIO_operator = operator_surname + ' ' + operator_name.split(' ')[0][0] + '.' + operator_name.split(' ')[1][
            0] + '.'

        date = request.POST.get('date').split('-')[2] + '.' + request.POST.get('date').split('-')[1] + '.' + \
               request.POST.get('date').split('-')[0]

        reports_to_print = Reports.objects.filter(structure=Structures.objects.get(employee=user),
                                                  date=request.POST.get('date'))
        int_units = ((u'рубль', u'рубля', u'рублей'), 'm')
        exp_units = ((u'копейка', u'копейки', u'копеек'), 'f')
        sum = 0
        nds = 0
        servs = ''
        for i, r in enumerate(reports_to_print):
            sum += r.sum
            nds += r.nds
            servs += f'\t{i + 1}. {r.service.name} {(str(r.sum).split(".")[0])} руб. {str("{:.2f}".format(r.sum)).split(".")[1]} коп. ({decimal2text(r.sum, int_units=int_units, exp_units=exp_units)}), ' \
                     f'в т.ч. НДС - {str(r.nds).split(".")[0]} руб. {str("{:.2f}".format(r.nds)).split(".")[1]} коп. ({decimal2text(r.nds, int_units=int_units, exp_units=exp_units)}).\n'

        data = {
            'res': f'Всего: {str("{:.2f}".format(sum)).split(".")[0]} руб. {str("{:.2f}".format(sum)).split(".")[1]} коп. ({decimal2text(sum, int_units=int_units, exp_units=exp_units)}), '
                   f'в т.ч. НДС – {str("{:.2f}".format(nds)).split(".")[0]} руб. {str("{:.2f}".format(nds)).split(".")[1]} коп.  ({decimal2text(nds, int_units=int_units, exp_units=exp_units)}).',
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

    return render(request, 'index.html', context)


def update_earned(request):
    sum = 0
    user = auth.get_user(request)
    groups = request.user.groups.values_list('name', flat=True)
    reports = Reports.objects.filter(structure=Structures.objects.get(employee=user),
                                     date__gte=f"{timezone.now().year}-01-01")
    for report in reports:
        sum += report.sum
    updSum = Structures.objects.get(employee=user)
    updSum.earned = sum
    updSum.save(update_fields=['earned'])
    return redirect(home)


@login_required
def dailyReport(request):
    user = auth.get_user(request)
    groups = request.user.groups.values_list('name', flat=True)
    context = {
        'menu': get_menu(groups),
        'userMenu': get_menu(groups),
        'title': 'Ежедневный отчет',
        'services': Services.objects.filter(
            structure=Structures.objects.get(employee=user)),
        'structure': Structures.objects.filter(employee=user)[0],
        'current_date': timezone.now(),
        'userAvatar': Profile.objects.get(user=request.user).avatar,
    }

    if request.method == 'POST':
        date = request.POST.get('service_date')
        service_id_list = request.POST.getlist('service_id')
        service_count_list = request.POST.getlist('service_count')

        for i in range(len(service_id_list)):
            sum = round(int(service_count_list[i]) * Services.objects.filter(pk=service_id_list[i])[0].price, 2)

            if int(service_count_list[i]) != 0:
                try:
                    report = Reports.objects.get(date=date, service=Services.objects.get(pk=service_id_list[i]),
                                                 structure=Structures.objects.filter(employee=user)[0])
                    report.amount = report.amount + int(service_count_list[i])
                    report.sum += sum
                    report.nds += round(sum / 6, 2)
                    report.save(update_fields=['amount', 'sum', 'nds'])
                except Reports.DoesNotExist:
                    Reports.objects.create(
                        date=date,
                        service=Services.objects.get(pk=service_id_list[i]),
                        structure=Structures.objects.filter(employee=user)[0],
                        amount=service_count_list[i],
                        sum=sum,
                        nds=round(sum / 6, 2)
                    )

                # report = Reports.objects.get(date=date, service=Services.objects.get(pk=service_id_list[i]),
                #                              structure=Structures.objects.filter(employee=Profile.objects.get(user=request.user))[0])
                # if report:
                #     report.amount += service_count_list[i]
                #     report.sum += sum
                #     report.nds += round(sum / 6, 2)
                #     report.save(update_fields=['amount', 'sum', 'nds'])
                # else:
                #     Reports.objects.create(
                #         date=date,
                #         service=Services.objects.get(pk=service_id_list[i]),
                #         structure=Structures.objects.filter(employee=Profile.objects.get(user=request.user))[0],
                #         amount=service_count_list[i],
                #         sum=sum,
                #         nds=round(sum / 6, 2)
                #     )

                updSum = Structures.objects.get(employee=user)
                updSum.earned += sum
                updSum.save(update_fields=['earned'])
            else:
                continue

        return redirect('home')

    return render(request, 'DailyReport.html', context)


@login_required
def chooseStructure(request):
    user = auth.get_user(request)
    groups = request.user.groups.values_list('name', flat=True)
    context = {
        'menu': get_menu(groups),
        'userMenu': get_menu(groups),
        'title': 'Выбор структуры',
        'structures': Structures.objects.all(),
        'userAvatar': Profile.objects.get(user=request.user).avatar,
    }

    return render(request, 'chooseStructure.html', context)


@login_required
def listReports(request, pk):
    user = auth.get_user(request)
    groups = request.user.groups.values_list('name', flat=True)
    context = {
        'menu': get_menu(groups),
        'userMenu': get_menu(groups),
        'title': 'Отчеты',
        'structure': Structures.objects.filter(pk=pk).first,
        'services': Services.objects.filter(structure=Structures.objects.get(pk=pk)),
        'reports': Reports.objects.filter(structure=pk, date__gte=f"{timezone.now().year}-01-01").order_by('-date'),
        'userAvatar': Profile.objects.get(user=request.user).avatar,
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

    return render(request, 'listReports.html', context)


def downloadReport(request):
    user = auth.get_user(request)
    groups = request.user.groups.values_list('name', flat=True)
    service = request.GET.get('service')
    date_start = request.GET.get('date_start')
    date_finish = request.GET.get('date_finish')
    structure = request.GET.get('structure')

    if 'Операторы' in groups:
        pk = Structures.objects.get(employee=user).pk
        reports = Reports.objects.filter(structure=Structures.objects.get(pk=pk))
    elif ('Экономисты' in groups or
          'Администраторы' in groups):
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
    user = auth.get_user(request)
    groups = request.user.groups.values_list('name', flat=True)
    context = {
        'menu': get_menu(groups),
        'user_menu': get_user_menu(groups),
        'title': 'Мои отчеты',
        'services': Services.objects.filter(
            structure=Structures.objects.get(employee=user)),
        'structure': Structures.objects.filter(employee=user).first,
        'reports': Reports.objects.filter(
            structure=Structures.objects.get(employee=user),
            date__gte=f"{timezone.now().year}-01-01").order_by('-date'),
        'userAvatar': Profile.objects.get(user=request.user).avatar,
    }
    if request.method == 'POST':
        pk = Structures.objects.get(employee=user)
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

    return render(request, 'listReports.html', context)


@login_required
def myServices(request):
    user = auth.get_user(request)
    groups = request.user.groups.values_list('name', flat=True)
    context = {
        'menu': get_menu(groups),
        'user_menu': get_user_menu(groups),
        'title': 'Мои услуги',
        'services': Services.objects.filter(
            structure=Structures.objects.get(employee=user)),
        # 'structure': Structures.objects.filter(employee=Profile.objects.get(user=request.user)).first,
        'userAvatar': Profile.objects.get(user=request.user).avatar,
    }

    if request.method == 'POST':
        pks = request.POST.getlist('pk')
        names = request.POST.getlist('name')
        descriptions = request.POST.getlist('description')
        prices = request.POST.getlist('price')

        for i in range(len(names)):
            Services.objects.filter(pk=pks[i]).update(name=names[i], description=descriptions[i], price=prices[i])

        return redirect('myServices')

    return render(request, 'my_services.html', context)


def del_service(request, pk):
    Services.objects.get(pk=pk).delete()
    return redirect(myServices)


@login_required
def newService(request):
    user = auth.get_user(request)
    groups = request.user.groups.values_list('name', flat=True)
    context = {
        'menu': get_menu(groups),
        'user_menu': get_user_menu(groups),
        'title': 'Новая услуга',
        'structure': Structures.objects.filter(employee=user).first,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        Services.objects.create(name=name, description=description, price=price,
                                structure=Structures.objects.filter(employee=user)[0])
        return redirect('myServices')

    return render(request, 'newService.html', context)

# @login_required
# def ibcNewOrder(request):
#     price = Services.objects.get(name='Печать').price
#     context = {
#         'title': 'Новый заказ',
#         'price': price
#     }
#
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         date_of_receiving = request.POST.get('date_of_receiving')
#         document = str(request.FILES['document']).replace(' ', '_')
#         comment = request.POST.get('comment')
#         #
#         # count_pages = len(PdfReader(document).pages)
#         # print(f'{count_pages} страниц')
#
#         order = Orders(service=Services.objects.get(pk=1),
#                        client_name=name,
#                        sum=0,
#                        email=email,
#                        phone=phone,
#                        date_of_receiving=date_of_receiving,
#                        comment=comment,
#                        file=request.FILES['document'],
#                        status='Заказ принят')
#         order.save()
#         print('save ok ----> ', document)
#         # doc = aw.Document(f'./uploads/ordersIBC/{strftime("%Y")}/{strftime("%m")}/{strftime("%d")}/{document}')
#         # Orders.objects.filter(pk=order.id).update(sum=price * doc.page_count)
#         # print('update ok ---> ', document)
#
#     return render(request, 'ibcNewOrder.html', context)

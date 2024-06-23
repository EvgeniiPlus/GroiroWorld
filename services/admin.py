from django.contrib import admin
from .models import *


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'structure', 'price')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_editable = ('price',)
    list_filter = ('structure',)


class StructuresAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'employee', 'plan', 'earned')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'employee')
    list_editable = ('employee',)


# class RolesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'description')
#     list_display_links = ('id', 'name')
#     search_fields = ('name',)
#
#
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('id', 'surname', 'name', 'role', 'email')
#     list_display_links = ('id', 'surname', 'name')
#     search_fields = ('surname', 'name')
#     list_editable = ('role', )
#     list_filter = ('role',)


class ReportsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'service', 'amount', 'sum', 'nds', 'date_create', 'date_edit')
    list_display_links = ('id', 'date', 'service')
    list_editable = ('nds',)
    list_filter = ('date', 'service', 'date_create')


# class OrdersAdmin(admin.ModelAdmin):
#     list_display = (
#     'id', 'service', 'client_name', 'sum', 'email', 'phone', 'date_of_receiving', 'status', 'date_create', 'date_edit')
#     list_display_links = ('id', 'service')
#     list_editable = ('status',)
#     list_filter = ('date_of_receiving', 'service', 'status', 'date_create')


admin.site.register(Services, ServicesAdmin)
admin.site.register(Structures, StructuresAdmin)
# admin.site.register(Roles, RolesAdmin)
# admin.site.register(Profile, ProfileAdmin)
admin.site.register(Reports, ReportsAdmin)
# admin.site.register(Orders, OrdersAdmin)

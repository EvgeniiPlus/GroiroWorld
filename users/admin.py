from django.contrib import admin
from openpyxl.pivot.cache import Groups

from .models import *


# class RolesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'description')
#     list_display_links = ('id', 'name')
#     search_fields = ('name',)


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'department')
    list_display_links = ('id', 'user')
    search_fields = ('user',)
    list_editable = ('department', )
    list_filter = ()

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_editable = ('short_name', )
    list_filter = ()

# admin.site.register(Roles, RolesAdmin)
admin.site.register(Profile, UsersAdmin)
admin.site.register(Department, DepartmentAdmin)

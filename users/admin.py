from django.contrib import admin
from openpyxl.pivot.cache import Groups

from .models import *


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')
    search_fields = ('user',)
    list_editable = ()
    list_filter = ()


admin.site.register(Profile, UsersAdmin)

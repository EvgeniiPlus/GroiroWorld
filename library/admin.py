from django.contrib import admin
from .models import *


class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'title', 'pub_place', 'publishing', 'pub_date', 'num_pages', 'invent_number', 'date_create')
    list_display_links = ('id', 'author', 'title',)
    search_fields = ('author', 'title')
    list_filter = ('author', 'publishing', 'pub_date')


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author_lastname', 'author_initials', 'title_article', 'title_magazine', 'pub_date', 'pub_number',
        'num_pages', 'date_create')
    list_display_links = ('id', 'author_lastname', 'author_initials', 'title_article')
    search_fields = ('author_lastname', 'title_article', 'title_magazine')
    list_filter = ('title_magazine', 'pub_date', 'pub_number')


class ReaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'work_place', 'telegram_id')
    list_display_links = ('name',)
    search_fields = ('name', 'telegram_id')
    list_filter = ('work_place', 'education')


class BookIssueAdmin(admin.ModelAdmin):
    list_display = ('book', 'reader', 'issue_date', 'is_return')
    list_display_links = ('book', 'reader')
    search_fields = ('book', 'reader', 'issue_date')
    list_filter = ('is_return',)


admin.site.register(Book, BookAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(BookIssue, BookIssueAdmin)

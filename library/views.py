import mimetypes
import os

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import StreamingHttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.core.paginator import Paginator
from docxtpl import DocxTemplate

from GroiroServices.settings import STATIC_URL
from .models import *
from users.models import *

main_menu = [{'title': 'Главная', 'url_name': 'lib_home', 'icon': 'fas fa-home fa-sm fa-fw me-2 text-gray-400',
              'role': ['Администраторы', 'Библиотекари']},
             {'title': 'Добавить книгу', 'url_name': 'new_book',
              'icon': 'fas fa-plus-square fa-sm fa-fw me-2 text-gray-400', 'role': ['Библиотекари']},
             {'title': 'Все книги', 'url_name': 'book_list',
              'icon': 'fas fa-book fa-sm fa-fw me-2 text-gray-400', 'role': ['Администраторы', 'Библиотекари']},
             {'title': 'Добавить статью', 'url_name': 'new_article',
              'icon': 'fas fa-plus-square fa-sm fa-fw me-2 text-gray-400', 'role': ['Библиотекари']},
             {'title': 'Все статьи', 'url_name': 'article_list',
              'icon': 'far fa-file-alt fa-sm fa-fw me-2 text-gray-400', 'role': ['Администраторы', 'Библиотекари']},
             ]

user_menu = [{'title': 'Профиль', 'url_name': 'profile', 'icon': 'fas fa-user fa-sm fa-fw me-2 text-gray-400',
              'role': ['Администраторы', 'Библиотекари']},
             {'title': 'Админ-панель', 'url_name': 'admin:index', 'icon': 'fas fa-cogs fa-sm fa-fw me-2 text-gray-400',
              'role': ['Администраторы']},
             {'title': 'Выйти', 'url_name': 'logout', 'icon': 'fas fa-sign-out-alt fa-sm fa-fw me-2 text-gray-400',
              'role': ['Администраторы', 'Библиотекари']},
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


# @login_required
# def index(request):
#     groups = request.user.groups.values_list('name', flat=True)
#
#     context = {
#         'menu': get_menu(groups),
#         'user_menu': get_user_menu(groups),
#         'title': 'ГрОИРО. Библиотека',
#         'userAvatar': Profile.objects.get(user=request.user).avatar,
#         'num_books': len(Book.objects.all()),
#         'num_articles': len(Article.objects.all()),
#         'last_books': Book.objects.all().order_by('date_create')[:10],
#         'last_articles': Article.objects.all().order_by('-date_create')[:10],
#     }
#
#     return render(request, 'lib_index.html', context=context)

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'lib_index.html'

    def get_context_data(self, **kwargs):
        groups = self.request.user.groups.values_list('name', flat=True)
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu(groups)
        context['user_menu'] = get_user_menu(groups)
        context['title'] = 'ГрОИРО. Библиотека'
        context['userAvatar'] = Profile.objects.get(user=self.request.user).avatar
        context['num_books'] = Book.objects.count()
        context['num_articles'] = Article.objects.count()
        context['last_books'] = Book.objects.all().order_by('-date_create')[:5]
        context['last_articles'] = Article.objects.all().order_by('-date_create')[:5]
        return context


# -------------------------------   views for books    ------------------------------------------
class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'lib_book_list.html'
    context_object_name = 'books'
    paginate_by = 50

    def get_queryset(self):
        return Book.objects.all().order_by('date_create')

    def get_context_data(self, **kwargs):
        groups = self.request.user.groups.values_list('name', flat=True)
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu(groups)
        context['user_menu'] = get_user_menu(groups)
        context['title'] = 'Все книги'
        context['userAvatar'] = Profile.objects.get(user=self.request.user).avatar
        return context


class NewBook(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'lib_new_book.html'
    success_url = reverse_lazy('lib_home')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        groups = self.request.user.groups.values_list('name', flat=True)
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu(groups)
        context['user_menu'] = get_user_menu(groups)
        context['title'] = 'Новая книга'
        context['userAvatar'] = Profile.objects.get(user=self.request.user).avatar
        return context


class ShowBook(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'lib_view_book.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        groups = self.request.user.groups.values_list('name', flat=True)
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu(groups)
        context['user_menu'] = get_user_menu(groups)
        context['title'] = Book.objects.get(id=self.kwargs['pk']).title
        context['userAvatar'] = Profile.objects.get(user=self.request.user).avatar
        return context


class UpdateBook(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'lib_edit_book.html'
    success_url = reverse_lazy('lib_home')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        groups = self.request.user.groups.values_list('name', flat=True)
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu(groups)
        context['user_menu'] = get_user_menu(groups)
        context['title'] = 'Редактирование книги'
        context['userAvatar'] = Profile.objects.get(user=self.request.user).avatar
        return context


def delete_book(request, pk):
    Book.objects.get(pk=pk).delete()
    return redirect('book_list')


def download_book(request, pk):
    book = Book.objects.get(pk=pk)
    data = {
        'index': book.index,
        'author': book.author,
        'author_mark': book.author_mark,
        'title': book.title,
        'pub_place': book.pub_place,
        'publishing': book.publishing,
        'pub_date': book.pub_date,
        'num_pages': book.num_pages,
        'invent_number': book.invent_number,
        'price': book.price,
        'number_of_copies': book.number_of_copies,
        'num_in_issue_book': book.num_in_issue_book,
    }

    doc = DocxTemplate("library/static/library/cardbook.docx")

    filename = f"Карточка для книги {data['invent_number']}.docx"
    filepath = f'library/static/library/cards/books/{filename}'
    doc.render(data)
    doc.save(filepath)

    chunk_size = 8192

    response = StreamingHttpResponse(FileResponse(open(filepath, 'rb'), chunk_size),
                                     content_type=mimetypes.guess_type(filepath)[0])

    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response


class SearchBook(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'lib_book_list.html'
    context_object_name = 'books'
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('search')
        return Book.objects.filter(Q(author__icontains=query) |
                                   Q(title__icontains=query) |
                                   Q(invent_number__icontains=query)).order_by('date_create')

    def get_context_data(self, **kwargs):
        groups = self.request.user.groups.values_list('name', flat=True)
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu(groups)
        context['user_menu'] = get_user_menu(groups)
        context['title'] = 'Результаты поиска'
        context['userAvatar'] = Profile.objects.get(user=self.request.user).avatar
        context['search_item'] = self.request.GET.get('search')
        return context


# -------------------------------   views for articles    ------------------------------------------

class CreateArticle(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'lib_new_article.html'
    success_url = reverse_lazy('lib_home')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        groups = self.request.user.groups.values_list('name', flat=True)
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu(groups)
        context['user_menu'] = get_user_menu(groups)
        context['title'] = 'Новая статья'
        context['userAvatar'] = Profile.objects.get(user=self.request.user).avatar
        return context


class ShowArticle(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'lib_view_article.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        groups = self.request.user.groups.values_list('name', flat=True)
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu(groups)
        context['user_menu'] = get_user_menu(groups)
        context['title'] = Article.objects.get(id=self.kwargs['pk']).title_article
        context['userAvatar'] = Profile.objects.get(user=self.request.user).avatar
        return context


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'lib_articles_list.html'
    context_object_name = 'articles'
    paginate_by = 50

    def get_queryset(self):
        return Article.objects.all().order_by('date_create')

    def get_context_data(self, **kwargs):
        groups = self.request.user.groups.values_list('name', flat=True)
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu(groups)
        context['user_menu'] = get_user_menu(groups)
        context['title'] = 'Все статьи'
        context['userAvatar'] = Profile.objects.get(user=self.request.user).avatar
        return context


class UpdateArticle(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'lib_edit_article.html'
    success_url = reverse_lazy('lib_home')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        groups = self.request.user.groups.values_list('name', flat=True)
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu(groups)
        context['user_menu'] = get_user_menu(groups)
        context['title'] = 'Редактирование статьи'
        context['userAvatar'] = Profile.objects.get(user=self.request.user).avatar
        return context


def delete_article(request, pk):
    Article.objects.get(pk=pk).delete()
    return redirect('article_list')


def download_cardarticle(request, pk):
    article = Article.objects.get(pk=pk)
    data = {
        'index': article.index,
        'author_initials': article.author_initials,
        'author_lastname': article.author_lastname,
        'title_article': article.title_article,
        'title_magazine': article.title_magazine,
        'pub_date': article.pub_date,
        'num_pages': article.num_pages,
        'pub_number': article.pub_number,
    }

    doc = DocxTemplate("library/static/library/cardarticle.docx")

    filename = f"Карточка для статьи {data['index']}.docx"
    filepath = f'library/static/library/cards/articles/{filename}'
    doc.render(data)
    doc.save(filepath)

    chunk_size = 8192

    response = StreamingHttpResponse(FileResponse(open(filepath, 'rb'), chunk_size),
                                     content_type=mimetypes.guess_type(filepath)[0])

    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response


class SearchArticle(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'lib_articles_list.html'
    context_object_name = 'articles'
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('search')
        return Article.objects.filter(Q(author_lastname__icontains=query) |
                                      Q(author_initials__icontains=query) |
                                      Q(title_article__icontains=query) |
                                      Q(title_magazine__icontains=query)).order_by('date_create')

    def get_context_data(self, **kwargs):
        groups = self.request.user.groups.values_list('name', flat=True)
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu(groups)
        context['user_menu'] = get_user_menu(groups)
        context['title'] = 'Результаты поиска'
        context['userAvatar'] = Profile.objects.get(user=self.request.user).avatar
        context['search_item'] = self.request.GET.get('search')
        return context

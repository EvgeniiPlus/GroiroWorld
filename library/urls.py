from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='lib_home'),
    # urls for books
    path('new_book', NewBook.as_view(), name='new_book'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', ShowBook.as_view(), name='show_book'),
    path('edit_book/<int:pk>', UpdateBook.as_view(), name='edit_book'),
    path('del_book/<int:pk>', delete_book, name='del_book'),
    path('download_book/<int:pk>', download_book, name='download_book'),
    path('search_book/', SearchBook.as_view(), name='search_book'),

    # urls for articles
    path('new_article', CreateArticle.as_view(), name='new_article'),
    path('article/<int:pk>/', ShowArticle.as_view(), name='show_article'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('edit_article/<int:pk>', UpdateArticle.as_view(), name='edit_article'),
    path('del_article/<int:pk>', delete_article, name='del_article'),
    path('search_article/', SearchArticle.as_view(), name='search_article'),
    path('download_cardarticle/<int:pk>', download_cardarticle, name='download_cardarticle'),

]

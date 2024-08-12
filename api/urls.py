from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('books/', views.BooksList.as_view()),
    path('book/<int:pk>/', views.BookDetal.as_view()),
    path('articles/', views.ArticlesList.as_view()),
    path('article/<int:pk>/', views.ArticleDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
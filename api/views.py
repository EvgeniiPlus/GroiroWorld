from rest_framework import generics
from . import serializers

from django.contrib.auth.models import User
from services.models import *
from users.models import *
from library.models import *


class BooksList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer


class ArticlesList(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer


class ArticleDetail(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer

from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers

from library.models import *


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer


class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = serializers.ReaderSerializer

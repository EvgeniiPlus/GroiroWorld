from rest_framework import serializers
from django.contrib.auth.models import User
from services.models import *
from users.models import *
from library.models import *


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'


class BookIssueSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title')

    class Meta:
        model = BookIssue
        fields = ['book_title', 'issue_date', 'is_return']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['book_title'] = representation['book_title'].replace('\r\n', '')
        return representation


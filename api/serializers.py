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

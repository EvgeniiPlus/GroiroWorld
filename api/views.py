from django.db.models import Q
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers

from library.models import *
from .serializers import BookIssueSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer

    @action(methods=['get'], detail=False)
    def search_by_pk(self, request):
        pk = request.query_params.get('pk', None)
        if pk:
            if Book.objects.filter(pk=pk).exists():
                book = Book.objects.get(pk=pk)
                serializers = self.get_serializer(book, many=False)
                return Response(serializers.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Book does not exists."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Book parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def search(self, request):
        query = request.query_params.get('query', None)
        print(query)
        if not query:
            return Response({"detail": "Необходимо указать поисковый запрос."}, status=status.HTTP_400_BAD_REQUEST)

        results = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query)).order_by('-date_create')

        if results.exists():
            serializers = self.get_serializer(results, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "По Вашему запросу книг не найдено."}, status=status.HTTP_404_NOT_FOUND)


class LastBooksView(generics.ListAPIView):
    serializer_class = serializers.BookSerializer

    def get_queryset(self):
        return Book.objects.order_by('-date_create')[:5]


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer


class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = serializers.ReaderSerializer

    @action(methods=['get'], detail=False)
    def search_by_telegram_id(self, request):
        telegram_id = request.query_params.get('telegram_id', None)
        if telegram_id:
            if Reader.objects.filter(telegram_id=telegram_id).exists():
                reader = Reader.objects.get(telegram_id=telegram_id)
                serializers = self.get_serializer(reader, many=False)
                return Response(serializers.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Reader does not exists."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Reader parameter is required."}, status=status.HTTP_400_BAD_REQUEST)


class BookIssueViewSet(viewsets.ModelViewSet):
    queryset = BookIssue.objects.all()
    serializer_class = serializers.BookIssueSerializer

    @action(methods=['post'], detail=False)
    def book_issue(self, request):
        book = Book.objects.get(id=request.data.get('book_id', None))
        reader = Reader.objects.get(id=Reader.objects.get(telegram_id=request.data.get('telegram_id', None)).pk)
        if book and reader:
            if BookIssue.objects.filter(book=book, reader=reader, is_return=False).exists():
                return Response({"detail": "Already exists"}, status=status.HTTP_200_OK)
            else:
                BookIssue.objects.create(book=book, reader=reader)
                return Response({"detail": "Book issued successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Reader or book not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False)
    def get_readers_books(self, request):
        telegram_id = request.query_params.get('telegram_id', None)

        if not telegram_id:
            return Response({"detail": "telegram_id parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            books = BookIssue.objects.filter(reader__telegram_id=telegram_id).order_by('-issue_date')
            if books.exists():
                serializers = BookIssueSerializer(books, many=True)
                return Response(serializers.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "No books were found for the current user."},
                                status=status.HTTP_404_NOT_FOUND)
        except Reader.DoesNotExist:
            return Response({"detail": "Reader with the provided telegram_id does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

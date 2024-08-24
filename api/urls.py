from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework import routers

from .views import LastBooksView

router = routers.DefaultRouter()

router.register(r'books', views.BookViewSet)
router.register(r'articles', views.ArticleViewSet)
router.register(r'readers', views.ReaderViewSet)
router.register(r'issues', views.BookIssueViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('last_books/', LastBooksView.as_view(), name='last_5_books')
]

# urlpatterns = format_suffix_patterns(urlpatterns)

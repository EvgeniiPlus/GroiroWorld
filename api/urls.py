from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r'books', views.BookViewSet)
router.register(r'articles', views.ArticleViewSet)
router.register(r'readers', views.ReaderViewSet)

print(router.urls)
urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)

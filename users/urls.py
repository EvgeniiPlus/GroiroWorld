from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path

from .views import *

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/logout/', user_logout, name='logout')

]

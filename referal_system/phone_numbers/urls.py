from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import IndexView, LoginView, VerifyView, update_user

app_name = 'phone'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('auth_code/', VerifyView.as_view(), name='auth_code'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(
        next_page='phone:login'), name='logout'),
    path('update/', update_user, name='update_code')
]

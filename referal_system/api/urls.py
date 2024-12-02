from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (MyProfileView, NewCodeView,
                    RegisterView, VerifyPhoneView,)

app_name = 'api'
router_v1 = DefaultRouter()


urlpatterns = [
    path('users/register/', RegisterView.as_view()),
    path('users/verify_code/', VerifyPhoneView.as_view()),
    path('users/new_code/', NewCodeView.as_view()),
    path('users/me/', MyProfileView.as_view()),
]

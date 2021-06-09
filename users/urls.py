from django.urls import path, include
from rest_framework import routers

from .views import RegisterAPI, LoginAPI, VerifyEmail

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    # path('<int:pk>/', AccountView.as_view(), name='user-account'),
    path('register', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    path('email-verify', VerifyEmail.as_view(), name='email-verify')
]
from django.urls import path, include
from rest_framework import routers

# from .views import AccountView
from .views import RegisterAPI, LoginAPI

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    # path('<int:pk>/', AccountView.as_view(), name='user-account'),
    path('register', RegisterAPI.as_view()),
    path('login', LoginAPI.as_view())
]
from django.urls import path, include
from rest_framework import routers

# from .views import AccountView

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    # path('<int:pk>/', AccountView.as_view(), name='user-account'),
]
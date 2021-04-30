from django.urls import path, include
from rest_framework import routers

from .views import ProfileView

router = routers.SimpleRouter()
# router.register(r'', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/profile/', ProfileView.as_view(), name='user-profile'),
]
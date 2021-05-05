from django.urls import path, include
from rest_framework import routers

# from .views import BookView

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    # path('<int:pk>/', BookView.as_view(), name='book'),
]
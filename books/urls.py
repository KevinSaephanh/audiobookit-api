from django.urls import path, include

from books.views import BookListAPIView, BookDetailAPIView

urlpatterns = [
    path('', BookListAPIView.as_view(), name='books'),
    path('<int:id>', BookDetailAPIView.as_view(), name='book')
]

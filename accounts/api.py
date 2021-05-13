from rest_framework import generics, permissions
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status

from .serializers import RegisterSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse('Account created!', status=status.HTTP_201_CREATED)
        else:
            return JsonResponse('Failed to create account', status=status.HTTP_400_BAD_REQUEST)

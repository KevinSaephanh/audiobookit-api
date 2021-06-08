from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, permissions
from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from utils.utils import Util
from .models import Account
from .serializers import RegisterSerializer, LoginSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            account_data = serializer.data
            account = Account.objects.get(email=account_data.email)

            token = RefreshToken.for_user(account).access

            current_site = get_current_site(request).domain
            relative_link = reverse('email-verify')

            absurl = 'http://' + current_site + relative_link + '?token=' + token
            email_body = 'Hello ' + account.username + ',\n\n Use the link below to verify your email:\n' + absurl
            data = {
                'email_body': email_body,
                'to_email': account.email,
                'email_subject': 'Verify Your Email'
            }
            Util.send_email(data)

            return JsonResponse('Account created!', status=status.HTTP_201_CREATED)
        else:
            return JsonResponse('Failed to create account', status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid:
            account = serializer.validated_data
            return JsonResponse(account, status=status.HTTP_200_OK)
        else:
            return JsonResponse('Unable to login', status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass

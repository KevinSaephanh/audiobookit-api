from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse
from rest_framework import generics, permissions
from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

from utils.utils import Util
from .models import User
from .serializers import RegisterSerializer, LoginSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Get user and token
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access

        # Get domain url
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        activation_link = 'http://' + current_site + relative_link + '?token=' + token

        # Create and send email
        email_body = 'Hello ' + user.username + ',\n\n Use the link below to verify your email:\n' + activation_link
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Verify Your Email'
        }
        Util.send_email(data)

        return JsonResponse('Account created!', status=status.HTTP_201_CREATED)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid:
            user = serializer.validated_data
            return JsonResponse(user, status=status.HTTP_200_OK)
        else:
            return JsonResponse('Unable to login', status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])

            if not user.is_active:
                user.is_active = True
                user.save()

            return JsonResponse({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Activation link has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

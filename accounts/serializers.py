from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'profile', 'books')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        account = Account.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return account


class LoginSerializer(serializers.ModelSerializer):
    id = serializers.CharField(max_length=30, min_length=3, read_only=True)
    username = serializers.CharField(max_length=30, min_length=3)
    password = serializers.CharField(max_length=100, min_length=7, write_only=True)
    email = serializers.CharField(max_length=50, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=50, min_length=3, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'password', 'tokens']

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        account = authenticate(username=username, password=password)

        # Check if account is inactive
        if not account.is_active:
            raise AuthenticationFailed('Account is inactive!')

        # Check if account is not null and is active
        if account is None:
            raise AuthenticationFailed('Wrong credentials provided!')

        update_last_login(None, account)
        return super().validate(data)

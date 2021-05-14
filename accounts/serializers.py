from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.http import Http404

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
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        account = authenticate(username = username, password = password)

        # Check if account is not null and is active
        if account is None or account.is_active:
            raise serializers.ValidationError('Wrong credentials provided!')

        # Get token and return account
        try:
            update_last_login(None, account)
            return {
                'id': account.get_user_id(),
                'username': account.username,
                'email': account.email,
                'profile': account.profile
            }
        except Account.DoesNotExist:
            raise Http404

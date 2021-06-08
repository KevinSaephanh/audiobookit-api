from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.exceptions import AuthenticationFailed

from utils.utils import Util
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', 'books')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=100, min_length=7, write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        if not Util.is_valid_username(username):
            raise serializers.ValidationError({
                'length': 'Username should be from 5 to 20 characters in length',
                'pattern': 'Username can contain alphanumeric characters as well as hyphens and underscores',
                'profanity': 'Username cannot contain profanity'
            })
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(max_length=30, min_length=3, read_only=True)
    username = serializers.CharField(max_length=30, min_length=3)
    password = serializers.CharField(max_length=100, min_length=7, write_only=True)
    email = serializers.CharField(max_length=50, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=50, min_length=3, read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password', 'tokens']

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)

        # Check if account is inactive
        if not user.is_active:
            raise AuthenticationFailed('Account is inactive!')

        # Check if account is not null and is active
        if user is None:
            raise AuthenticationFailed('Wrong credentials provided!')

        update_last_login(None, user)
        return super().validate(data)

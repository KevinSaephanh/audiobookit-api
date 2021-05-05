from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'],
            validated_data['username'],
            None,
            validated_data['password']
        )
        return user

class AccountSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
                queryset=get_user_model().objects.all())

    class Meta:
        model = Account
        fields = ('__all__')
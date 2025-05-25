from os import access

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    role = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, required=True)


    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.username = validated_data.get('username', instance.username)

        if 'password' in validated_data:
            instance.password = make_password(validated_data['password'])

        instance.save()
        return instance




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data.update({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': self.user.id,
                'role': self.user.role,
                'username': self.user.username
            }
        })

        return data

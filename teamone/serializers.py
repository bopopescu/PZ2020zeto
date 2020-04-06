from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Schronisko, Zwierze, Lista
from django.contrib.auth.models import User


class SchroniskoSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Schronisko
        fields = '__all__'

class ZwierzeSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Zwierze
        fields = '__all__'

class ListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lista
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['user_id']

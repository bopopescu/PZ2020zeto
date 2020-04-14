from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Schronisko, Zwierze, Lista, Preferencje
from django.contrib.auth.models import User


class SchroniskoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schronisko
        fields = '__all__'

class ZwierzeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zwierze
        fields = '__all__'

    def create(self, validated_data):
        return Zwierze.objects.create(**validated_data)

class ListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lista
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class PreferencjeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preferencje
        fields = ['czyDuzeMieszkanie', 'czyDuzoCzasu', 'czyDzieci']

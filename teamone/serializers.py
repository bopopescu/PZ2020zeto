from rest_framework import serializers
from .models import Schronisko, Zwierze
from django.contrib.auth.models import User


class SchroniskoSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Schronisko
        fields = '__all__'


class ZwierzeSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Zwierze
        fields = '__all__'
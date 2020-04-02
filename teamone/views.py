from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import Schronisko, Zwierze
from .serializers import SchroniskoSeralizer, ZwierzeSeralizer
from rest_framework.parsers import JSONParser
from django.template import loader
from django.contrib.auth.models import User
# Create your views here.


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


class ZwierzetaLista(generics.ListAPIView):
    queryset = Zwierze.objects.all()
    serializerClass = ZwierzeSeralizer

    def get(self, request):
        zw = Zwierze.objects.all()
        serializer = ZwierzeSeralizer(zw, many = True)
        return JsonResponse(serializer.data, safe = False)

class ZwierzetaDetail(generics.RetrieveAPIView):
    queryset = Zwierze.objects.all()
    serializerClass = ZwierzeSeralizer

    def get(self, request, pk):
        zwierzak = Zwierze.objects.filter(id=pk)
        serializer = ZwierzeSeralizer(zwierzak, many=True)
        return JsonResponse(serializer.data, safe = False)


class ZwierzetaFiltry(generics.ListAPIView):
    queryset = Zwierze.objects.all()
    serializer_class = ZwierzeSeralizer

    def get(self, request, filtr):
        if(filtr[0] == '1'):
            lista = Zwierze.objects.filter(czyDuzeMieszkanie=filtr[1], czyDuzoCzasu=filtr[2], czyDzieci=filtr[3])
        else:
            lista = Zwierze.objects.all()
        serializer = ZwierzeSeralizer(lista, many = True)
        return JsonResponse(serializer.data, safe = False)

from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import Schronisko, Zwierze
from .serializers import SchroniskoSeralizer, ZwierzeSeralizer, UserSerializer, TokenSerializer
from rest_framework.parsers import JSONParser
from django.template import loader
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from teamone.serializers import UserSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework.authtoken.models import Token

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

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            Token.objects.create(user = request.user)
            return redirect('login.html')
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("http://77.55.237.205:8100/page/main")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form" : form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('http://77.55.237.205:8000/accounts/login/')

class NameView(generics.RetrieveAPIView):
    queryset = Zwierze.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        user = User.objects.filter(username=request.user.username)
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)

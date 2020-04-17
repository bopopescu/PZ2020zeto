from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import  Zwierze, Preferencje
from .serializers import ZwierzeSerializer, PreferencjeSerializer, PreferencjePostSerializer
from django.template import loader
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from teamone.serializers import UserSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


class ZwierzetaLista(generics.ListAPIView):
    queryset = Zwierze.objects.all()
    serializerClass = ZwierzeSerializer

    def get(self, request):
        zw = Zwierze.objects.all()
        serializer = ZwierzeSerializer(zw, many = True)
        return JsonResponse(serializer.data, safe = False)

class ZwierzetaDetail(generics.RetrieveAPIView):
    queryset = Zwierze.objects.all()
    serializerClass = ZwierzeSerializer

    def get(self, request, pk):
        zwierzak = Zwierze.objects.filter(id=pk)
        serializer = ZwierzeSerializer(zwierzak, many=True)
        return JsonResponse(serializer.data, safe = False)


class ZwierzetaFiltry(generics.ListAPIView):
    queryset = Zwierze.objects.all()
    serializer_class = ZwierzeSerializer

    def get(self, request, filtr):
        if(filtr[0] == '1'):
            lista = Zwierze.objects.filter(czyDuzeMieszkanie=filtr[1], czyDuzoCzasu=filtr[2], czyDzieci=filtr[3])
        else:
            lista = Zwierze.objects.all()
        serializer = ZwierzeSerializer(lista, many = True)
        return JsonResponse(serializer.data, safe = False)

"""
@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('http://77.55.237.205:8000/login/')
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {'form': form})

@csrf_exempt
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

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('http://77.55.237.205:8000/login/')
"""

class NameView(generics.RetrieveAPIView):
    queryset = Zwierze.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        user = User.objects.filter(username=self.request.user.get_username())
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)

class ZwierzePost(generics.ListCreateAPIView):
    queryset = Zwierze.objects.all()
    serializer_class = ZwierzeSerializer
    def perform_create(self, serializer_class):
        serializer_class.save()

class PreferencjeGet(generics.RetrieveAPIView):
    queryset = Preferencje.objects.all()
    serializer_class = PreferencjeSerializer

    def get(self, request, token):
        preferencje = Preferencje.objects.filter(token_user=token)
        serializer = PreferencjeSerializer(preferencje, many=True)
        return JsonResponse(serializer.data, safe=False)

class PreferencjePut(generics.UpdateAPIView):
    queryset = Preferencje.objects.all()
    serializer_class = PreferencjeSerializer

class PreferencjePost(generics.ListCreateAPIView):
    queryset = Preferencje.objects.all()
    serializer_class = PreferencjePostSerializer

    def perform_create(self, serializer_class):
        serializer_class.save()
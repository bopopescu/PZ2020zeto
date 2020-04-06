from django.db.models import Max
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

# Create your views here.
from django.utils.functional import SimpleLazyObject

from teamone.serializers import UserSerializer


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("http://77.55.237.205:8100/page/main")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form":form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('http://77.55.237.205:8000/accounts/login/')

def name_view(request):
    lista = User.objects.order_by('-last_login')
    serializer = UserSerializer(lista, many=True)
    return JsonResponse(serializer.data[0], safe=False)
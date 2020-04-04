from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from teamone.models import Uzytkownik

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            Uzytkownik.objects.create(login=username, haslo=password, lajk= 1)
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
            return redirect("77.55.237.205:8100/page/main")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form":form})
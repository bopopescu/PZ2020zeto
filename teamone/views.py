import token

from django.views.generic import ListView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Zwierze, Preferencje, Schronisko, BWLista
from .serializers import ZwierzeSerializer, PreferencjeSerializer, PreferencjePostSerializer, SchroniskoSerializer, ListaSerializer
from django.template import loader
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from teamone.serializers import UserSerializer
from itertools import chain

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

class ZwierzetaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zwierze.objects.all()
    serializer_class = ZwierzeSerializer

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



class ZwierzeFiltr(ListView):

    def get(self, request, token):
        if True:
            pref = Preferencje.objects.get(token_user=token)

            # zw = ZwierzetaLista.objects.filter(
            #    czyDuzeMieszkanie = Preferencje.objects.values_list('czyDuzeMieszkanie', flat = True).filter(token_user = token),
            #    czyDuzoCzasu = Preferencje.objects.values_list('czyDuzoCzasu', flat = True).filter(token_user = token),
            #    czyDzieci = Preferencje.objects.values_list('czyDzieci', flat = True).filter(token_user = token)
            # )

            zw = Zwierze.objects.filter(
                czyDuzeMieszkanie=pref.czyDuzeMieszkanie,
                czyDuzoCzasu=pref.czyDuzoCzasu,
                czyDzieci=pref.czyDzieci
            )
            zww = list()
            for c in zw.iterator():
                wyswietlony = BWLista.objects.filter(token_user=token, zwierzeID_id=c.id).count()
                if wyswietlony == 0:
                    zww += Zwierze.objects.filter(id=c.id)
            serializer = ZwierzeSerializer(zww, many=True)

            return JsonResponse(serializer.data, safe=False)

class ZwierzeUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = ZwierzeSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NazwaSchronisko(APIView):
    def get(self, request):
        queryset = Schronisko.objects.all()
        serializer = SchroniskoSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

class WList(generics.RetrieveAPIView):
    queryset = BWLista.objects.all()
    serializer_class = ListaSerializer

    def get(self, request, token):
        lst = BWLista.objects.filter(token_user = token, czyLike = "True")
        queryset = list()
        for z in lst.iterator():
            queryset += Zwierze.objects.filter(id=z.zwierzeID.id)   #działa, nie zastanawiaj się ;_;
        serializer = ZwierzeSerializer(queryset, many=True)
        return Response(serializer.data)

class WListDelete(APIView):
    queryset = BWLista.objects.all()
    serializer_class = ListaSerializer

    def delete(self, request, pk, token):
        zw = BWLista.objects.get(zwierzeID_id=pk, token_user = token)
        zw.delete()
        return HttpResponse('yay', status=status.HTTP_200_OK)

class BWListPut(generics.ListCreateAPIView):
    serializer_class = ListaSerializer

    def get(self, request, *args, **kwargs):
        serializer = ListaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BList(ListView):
    def get(self, request, token):
        lst = BWLista.objects.filter(token_user = token, czyLike = "False")
        queryset = list()
        for z in lst.iterator():
            queryset += Zwierze.objects.filter(id=z.zwierzeID.id)   #działa, nie zastanawiaj się ;_;
        serializer = ZwierzeSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

class Superuser(APIView):
    def get(self, request, token):
        user_id = Token.objects.get(key=token)
        czy_superuser = User.objects.get(id=user_id.user_id)
        serializer=UserSerializer(czy_superuser)
        return JsonResponse(serializer.data, safe=False)
        #serializer=UserSerializer(czy_superuser)
        #return Response(serializer.data)
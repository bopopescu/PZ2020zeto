from django.views.generic import ListView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Zwierze, Preferencje, Schronisko, BWLista
from .serializers import ZwierzeSerializer, PreferencjeSerializer, PreferencjePostSerializer, SchroniskoSerializer, ListaSerializer
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from teamone.serializers import UserSerializer

#Paweł
class ZwierzetaLista(generics.ListAPIView):
    queryset = Zwierze.objects.all()
    serializerClass = ZwierzeSerializer

    def get(self, request):
        zw = Zwierze.objects.all()
        serializer = ZwierzeSerializer(zw, many=True)
        return JsonResponse(serializer.data, safe=False)

#Adrian
class ZwierzetaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zwierze.objects.all()
    serializer_class = ZwierzeSerializer

#Adrian
class NameView(generics.RetrieveAPIView):
    queryset = Zwierze.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        user = User.objects.filter(username=self.request.user.get_username())
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)

#Adrian
class ZwierzePost(generics.ListCreateAPIView):
    queryset = Zwierze.objects.all()
    serializer_class = ZwierzeSerializer
    def perform_create(self, serializer_class):
        serializer_class.save()

#Adrian
class PreferencjeGet(generics.RetrieveAPIView):
    queryset = Preferencje.objects.all()
    serializer_class = PreferencjeSerializer

    def get(self, request, token):
        preferencje = Preferencje.objects.filter(token_user=token)
        serializer = PreferencjeSerializer(preferencje, many=True)
        return JsonResponse(serializer.data, safe=False)

#Adrian
class PreferencjePut(generics.UpdateAPIView):
    queryset = Preferencje.objects.all()
    serializer_class = PreferencjeSerializer

#Adrian
class PreferencjePost(generics.ListCreateAPIView):
    queryset = Preferencje.objects.all()
    serializer_class = PreferencjePostSerializer

    def perform_create(self, serializer_class):
        serializer_class.save()

#Paweł
class ZwierzeFiltr(ListView):

    def get(self, request, token):
        if True:
            pref = Preferencje.objects.get(token_user=token)
            zw = Zwierze.objects.filter(
                czyDuzeMieszkanie=pref.czyDuzeMieszkanie,
                czyDuzoCzasu=pref.czyDuzoCzasu,
                czyDzieci=pref.czyDzieci
            )
            zww = list()
            for c in zw.iterator():
                wyswietlony = BWLista.objects.filter(token_user_id=token, zwierzeID_id=c.id).count()
                if wyswietlony == 0:
                    zww += Zwierze.objects.filter(id=c.id)
            serializer = ZwierzeSerializer(zww, many=True)
            return JsonResponse(serializer.data, safe=False)

#Adrian
class ZwierzeUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = ZwierzeSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Adrian
class NazwaSchronisko(ListView):
    def get(self, request):
        queryset = Schronisko.objects.all()
        serializer = SchroniskoSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

#Paweł
class WList(generics.RetrieveAPIView):
    queryset = BWLista.objects.all()
    serializer_class = ListaSerializer

    def get(self, request, token):
        lst = BWLista.objects.filter(token_user_id = token, czyLike = "True")
        queryset = list()
        for z in lst.iterator():
            queryset += Zwierze.objects.filter(id=z.zwierzeID.id)   #działa, nie zastanawiaj się ;_;
        serializer = ZwierzeSerializer(queryset, many=True)
        return Response(serializer.data)

#Paweł
class WListDelete(APIView):
    queryset = BWLista.objects.all()
    serializer_class = ListaSerializer

    def delete(self, request, pk, token):
        zw = BWLista.objects.get(zwierzeID_id=pk, token_user_id = token)
        zw.delete()
        return HttpResponse('yay', status=status.HTTP_200_OK)

#Paweł
class BWListPut(generics.ListCreateAPIView):
    serializer_class = ListaSerializer

    def get(self, request, *args, **kwargs):
        serializer = ListaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Paweł
class BList(ListView):
    def get(self, request, token):
        lst = BWLista.objects.filter(token_user_id = token, czyLike = "False")
        queryset = list()
        for z in lst.iterator():
            queryset += Zwierze.objects.filter(id=z.zwierzeID.id)   #działa, nie zastanawiaj się ;_;
        serializer = ZwierzeSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

#Adrian
class Superuser(APIView):
    def get(self, request, token):
        user_id = Token.objects.get(key=token)
        czy_superuser = User.objects.get(id=user_id.user_id)
        serializer=UserSerializer(czy_superuser)
        return JsonResponse(serializer.data, safe=False)

#Adrian
class AddSchronisko(APIView):
    def post(self, request, name):
        serializer = SchroniskoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            superuser = User.objects.filter(username=name).update(is_staff=1)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Adrian
class UpdateSchronisko(generics.RetrieveUpdateAPIView):
    queryset = Schronisko.objects.all()
    serializer_class = SchroniskoSerializer

#Paweł
class DeleteSchronisko(generics.RetrieveAPIView):
    queryset = Schronisko.objects.all()
    serializer_class = SchroniskoSerializer

    def deleteuser(self, pk):
        user = User.objects.get(id=pk)
        user.delete()
        return Response(status=status.HTTP_200_OK)

    def deletepref(self, token):
        pref = Preferencje.objects.get(token_user=token)
        pref.delete()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        schronisko = Schronisko.objects.get(token=pk)
        serializer = SchroniskoSerializer(schronisko)
        schronisko.delete()
        userid = Token.objects.get(key=pk)
        userid2 = userid.user_id
        self.deleteuser(userid2)
        self.deletepref(pk)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Adrian
class DeleteUser(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#Adrian
class ZwierzSchronGet(ListView):
    def get(self, request, token):
        queryset = Zwierze.objects.filter(schroniskoID_id=token)
        serializer = ZwierzeSerializer(queryset,many=True)
        return JsonResponse(serializer.data, safe=False)

#Adrian
class ZwierzSchronDelete(APIView):
    def delete(self, request, token, pk):
        queryset = Zwierze.objects.get(schroniskoID_id=token, id=pk)
        queryset.delete()
        return HttpResponse('yay', status=status.HTTP_200_OK)

#Adrian
class ZwierzSchronUpdate(generics.RetrieveUpdateAPIView):
    queryset = Zwierze.objects.all()
    serializer_class = ZwierzeSerializer
from django.db import models


class Schronisko(models.Model):
    login = models.CharField(max_length=30)
    haslo = models.CharField(max_length=30)
    telefon = models.CharField(max_length=15)
    adres = models.CharField(max_length=30)

class Uzytkownik(models.Model):
    login = models.CharField(max_length=30)
    haslo = models.CharField(max_length=30)
    lajk = models.BooleanField()

class Zwierze(models.Model):
    schroniskoID = models.ForeignKey(Schronisko, on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=30)
    gatunek = models.CharField(max_length=30)
    zdjecie = models.CharField(max_length=50)
    opis = models.CharField(max_length=200)
    czyDuzeMieszkanie = models.BooleanField()
    #czyMaleMieszkanie = models.BooleanField()
    czyDuzoCzasu = models.BooleanField()
    #czyMaloCzasu = models.BooleanField()
    czyDzieci = models.BooleanField()

class Lista(models.Model):
    uzytkownikID = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    zwierzeID = models.ForeignKey(Zwierze, on_delete=models.CASCADE)



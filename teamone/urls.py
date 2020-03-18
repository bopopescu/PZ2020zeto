from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name ='index'),
    path('zwierzaki', views.ZwierzetaLista.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
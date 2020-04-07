from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from teamone import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url



router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name ='index'),
    path('zwierzaki', views.ZwierzetaLista.as_view()),
    path('zwierzaki/<int:pk>', views.ZwierzetaDetail.as_view()),
    path('zfiltr/<str:filtr>', views.ZwierzetaFiltry.as_view()),
    url(r'^signup/$', views.signup_view, name="signup"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^name', views.NameView.as_view()),
    url(r'^zwierzePost', views.ZwierzePost.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
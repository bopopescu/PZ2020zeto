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
    path('zfiltr/<str:token>', views.ZwierzeFiltr.as_view()),
    #url(r'^signup/$', views.signup_view, name="signup"),
    #url(r'^login/$', views.login_view, name="login"),
    #url(r'^logout/$', views.logout_view, name="logout"),
    path('name', views.NameView.as_view()),
    path('zwierzePost', views.ZwierzePost.as_view()),
    path('PreferencjeGet/<str:token>', views.PreferencjeGet.as_view()),
    path('PreferencjePut/<str:pk>', views.PreferencjePut.as_view()),
    path('PreferencjePost', views.PreferencjePost.as_view()),
    path('ZwierzeAdd', views.ZwierzeUploadView.as_view()),
    path('SchroniskoNazwa', views.NazwaSchronisko.as_view()),
    path('WList/<str:token>', views.WList.as_view()),
    path('BList/<str:token>', views.BList.as_view()),
    path('BWListPut/<str:token>', views.BWListPut.as_view()),
    path('WListDelete/<int:pk>', views.WListDelete.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
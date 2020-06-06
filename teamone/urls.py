from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from teamone import views
from rest_framework.urlpatterns import format_suffix_patterns

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('zwierzaki', views.ZwierzetaLista.as_view()),
    path('zwierzaki/<int:pk>', views.ZwierzetaDetail.as_view()),
    path('zfiltr/<str:token>', views.ZwierzeFiltr.as_view()),
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
    path('WListDelete/<str:token>/<int:pk>', views.WListDelete.as_view()),
    path('SuperUser/<str:token>', views.Superuser.as_view()),
    path('SchroniskoAdd/<str:name>', views.AddSchronisko.as_view()),
    path('SchroniskoUpdate/<str:pk>', views.UpdateSchronisko.as_view()),
    path('SchroniskoDelete/<str:pk>', views.DeleteSchronisko.as_view()),
    path('UserDelete/<int:pk>', views.DeleteUser.as_view()),
    path('ZSGet/<str:token>', views.ZwierzSchronGet.as_view()),
    path('ZSDelete/<str:token>/<int:pk>', views.ZwierzSchronDelete.as_view()),
    path('ZSUpdate/<str:token>/<int:pk>', views.ZwierzSchronUpdate.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
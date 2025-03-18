from django.urls import path
from . import views
app_name = 'atxaisoft'  # Uygulama adı tanımlandı
urlpatterns = [

    path('', views.index, name='index'),

]

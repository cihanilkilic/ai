from django.urls import path
from . import views
app_name = 'asistan'  # Uygulama adı tanımlandı
urlpatterns = [

    path("asistan/", views.asistan, name="asistan"),
    path("speech_to_text/", views.speech_to_text, name="speech_to_text"),

]

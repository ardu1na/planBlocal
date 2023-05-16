
from django.urls import path
from whatsapp.views import sendwhats

urlpatterns = [
    path('send/', sendwhats, name="send"),
]

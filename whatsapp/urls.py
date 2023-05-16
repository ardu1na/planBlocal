
from django.urls import path
from whatsapp.views import sendwhats, index

urlpatterns = [
    path('send/', sendwhats, name="send"),
    path('', index, name="index"),

]


from django.urls import path
from whatsapp.views import sendwhats, index, logs

urlpatterns = [
    path('send/', sendwhats, name="send"),
    path('', index, name="index"),
    path('logs/', logs, name="logs"),
]

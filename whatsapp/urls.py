
from django.urls import path
from whatsapp.views import sendwhats, index, logs, log_download

urlpatterns = [
    path('send/', sendwhats, name="send"),
    path('', index, name="index"),
    path('logs/', logs, name="logs"),
    path('logs/download/', log_download, name='log_download'),

]

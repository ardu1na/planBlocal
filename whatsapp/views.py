import pywhatkit
from django.http import HttpResponse
from urllib.request import urlopen
import json
import time
from whatsapp.models import LastAlert
from django.shortcuts import render, redirect

def index  (request):
    template = 'index.html'
    context = {}
    return render (request, template, context)

def sendwhats(request):
    url = "http://200.58.105.20/api/alarms/"
    
    
    response = urlopen(url)
    data = json.loads(response.read())
    print(data)
    
    miembro = data['miembro']
    tipo = data ['tipo']
    lugar = data['vivienda']
    group = data ['wp']
    datetime = data ['datetime']
    
    last = LastAlert.objects.first()

    if last is None:
        print("create first instance ")

        new = LastAlert.objects.create(datetime=datetime)
        print("done")

    elif last.datetime != datetime:
        print("new data, updating lastalert")

        last.datetime=datetime
        last.save()
        print("done")

        message = f'ALERTA {tipo} de {miembro} \n {lugar}'
        #pywhatkit.sendwhatmsg_to_group_instantly(group, message)
        #time.sleep(25)
    
    else:
        print("no new alerts yet")
    
    return redirect('index')


    


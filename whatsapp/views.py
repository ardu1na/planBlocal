import pywhatkit
from django.http import HttpResponse
from urllib.request import urlopen
import json
from datetime import datetime, date
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
    strdatetime = data ['datetime']
    datetime_format = "%Y-%m-%d %H:%M:%S"
    ddatetime = datetime.strptime(strdatetime, datetime_format)

    last = LastAlert.objects.first()



    print (f'from api date= {strdatetime} \n from db date ={last.datetime}')
    
    
    if last is None:
        print("create first instance ")
        first = LastAlert.objects.create(datetime=date.now())
        print("done")
        
        
        
    elif last.datetime != ddatetime:
        print("new data, updating lastalert")

        last.datetime=ddatetime
        last.save()
        print("done")

        message = f'ALERTA {tipo} de {miembro} \n {lugar}'
        #pywhatkit.sendwhatmsg_to_group_instantly(group, message)
        #time.sleep(25)
    
    else:
        print("no new alerts yet")
    
    return redirect('index')


    


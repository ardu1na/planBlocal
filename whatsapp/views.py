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

def sendwhats(request): # IN LINE 121     tab_close: bool = True, LIB/PYWHATKIT/WHATS.PY  SET CLOSE_TAB = TRUE

    url = "http://200.58.105.20/api/alarms/"
    
    
    response = urlopen(url)
    data = json.loads(response.read())
    print(f'data from api: \n {data}')
    
    miembro = data['miembro']
    tipo = data ['tipo']
    lugar = data['vivienda']
    group =  'LkNG4BNQsXK2Xfn99DwbFV' #data ['wp']
    strdatetime = data ['datetime']
    datetime_format = "%Y-%m-%d %H:%M:%S"
    ddatetime = datetime.strptime(strdatetime, datetime_format)

    last = LastAlert.objects.first()   
    
    if last is None:
        print("create first instance ")
        first = LastAlert.objects.create(datetime=date.now())
        print("done")
        return redirect('index')

        
        
    elif last.datetime != ddatetime:
        print("new data, updating lastalert")

        last.datetime=ddatetime
        last.save()
        print("done")

    
    
    else:
    
        print("no new alerts yet")
    
    message = f'ALERTA {tipo} de {miembro} \n {lugar}'
    pywhatkit.sendwhatmsg_to_group_instantly(group, message)
    return HttpResponse("going to wsp...")

     #redirect('index')


    


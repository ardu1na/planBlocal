import pywhatkit
from django.http import JsonResponse
from urllib.request import urlopen
import json
from datetime import datetime, date
from whatsapp.models import LastAlert
from django.shortcuts import render, redirect




## TODO
# añadir instrucciones e introducción al bot
# añadir autentificación a la API
# alerta al final una que cambia y se cierra sola
# añadir link al registro de mensajes y al sitio web oficial


def index  (request): 
    template = 'monitor.html'
    context = {}
    return render (request, template, context)

def sendwhats(request): # IN LINE 121     tab_close: bool = True, LIB/PYWHATKIT/WHATS.PY  SET CLOSE_TAB = TRUE

    url = "http://200.58.105.20/api/alarms/"
    
    
    try:
        response = urlopen(url)
        data = json.loads(response.read())
        
        
        strdatetime = data ['datetime']
        datetime_format = "%Y-%m-%d %H:%M:%S"
        ddatetime = datetime.strptime(strdatetime, datetime_format)

        last = LastAlert.objects.first()   
        
        if last is None:
            print("create first instance ")
            first = LastAlert.objects.create(datetime=date.now())
            print("done")
           
            
        elif last.datetime != ddatetime:

            print("new data, updating lastalert")
            print()
            print(f'data from api: \n {data}')

            last.datetime=ddatetime
            last.save()
            print("done") 
            
            
            
            
            miembro = data['miembro']
            tipo = data ['tipo']
            lugar = data['vivienda']
            group =  'LkNG4BNQsXK2Xfn99DwbFV' #data ['wp']
            
            message = f'ALERTA {tipo} de {miembro} \n {lugar}'
            
            pywhatkit.sendwhatmsg_to_group_instantly(group, message)
            
            print(f'message: {message} sent !!')
            
                   
        else:        
            print("no new alerts yet")
        
        

    
    except:
        print(" . ")
        print(" ..")
        print("... something get wrong with api conection")
        print("......................  . .lets try again ... ")

    return JsonResponse(data)
        



    


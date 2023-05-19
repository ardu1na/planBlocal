import pywhatkit
from django.http import JsonResponse, HttpResponse
from urllib.request import urlopen
import json
from datetime import datetime, date
from whatsapp.models import LastAlert
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator

## TODO
# añadir instrucciones e introducción al bot
# key API
# añadir link a la webapp en prod


def index  (request): 
    template = 'monitor.html'
    context = {}
    return render (request, template, context)

def sendwhats(request):

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
            group = data ['wp']
            
            message = f'ALERTA {tipo} de {miembro} \n {lugar}'
            try:
                pywhatkit.sendwhatmsg_to_group_instantly(group, message)
                print(f'message: {message} sent !!')

            except:
                error_message = f'No se ha podido enviar el mensaje. \n {message}\n Por favor verifica el id del grupo de WhatsApp.'
                messages.error(request, error_message)
                return redirect('index')
                               
        else:        
            print("no new alerts yet")   
        
        return JsonResponse(data)  

    
    except:
        print(" . ")
        print(" ..")
        print("... something get wrong with api conection")
        error_message = f'Ups! \n Algo salió mal estableciendo la conexión. \n Si el problema persiste, por favor contacta al administrador.'
        messages.error(request, error_message)  
        return redirect('index')
        

        
def logs(request):
    with open('PyWhatKit_DB.txt', 'r') as file:
        log_entries = []
        entry = {}
        for line in file:
            if line.strip() == '--------------------':
                if entry:
                    log_entries.append(entry)
                    entry = {}
            else:
                key, value = line.strip().split(': ', 1)
                entry[key.lower().replace(' ', '_')] = value
        if entry:
            log_entries.append(entry)

    paginator = Paginator(log_entries, 5)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = 'logs.html'
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)




def log_download(request):
    with open('PyWhatKit_DB.txt', 'r') as file:
        response = HttpResponse(file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="log.txt"'
        return response

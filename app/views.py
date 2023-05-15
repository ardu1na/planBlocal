import pywhatkit
from django.shortcuts import render
from urllib.request import urlopen
import json



def index (request):
    template = 'index.html'
    url = "http://200.58.105.20/api/alarms/"
    
    try:
        response = urlopen(url)
        data = json.loads(response.read())
        miembro = data['miembro']
        tipo = data ['tipo']
        lugar = data['vivienda']
        group = data ['wp']
        message = f'ALERTA {tipo} de {miembro} \n {lugar}'
        pywhatkit.sendwhatmsg_to_group_instantly(group, message)

    except:
        print ("Something get wrong sending message or gettin data from API")
    context = {}
    return render (request, template, context)


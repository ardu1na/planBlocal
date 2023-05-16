import pywhatkit
from django.http import HttpResponse
from urllib.request import urlopen
import json
import time



def index (request):
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
        time.sleep(25)
        return HttpResponse(status=204)
    except:
        print ("Something get wrong sending message or gettin data from API")
    
    


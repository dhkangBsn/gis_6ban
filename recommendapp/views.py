from django.core.serializers import serialize
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView

import requests
import json

def main_html(request):
    return render(request, 'recommendapp/main_html.html', {})

URL = 'http://15.164.232.127:5000/recommend'
headers = {'User-Agent': 'Mozila/5.0'}

def recommend(request):
    try:
        name = request.POST['name']
        print('name', name)
        payload = {'name': str(name)}
        session = requests.Session()
        res = session.post(URL, headers=headers, data=payload)
        print(res.text)
        result = json.loads(res.text)
        print(result)
        session.close()
        return render(request, 'recommendapp/recommend.html', {'result':result['emotion_title']})
    except:
        return render(request, 'recommendapp/main_html.html', {})



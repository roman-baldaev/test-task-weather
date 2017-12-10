from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from . import last_update
import json


def index(request):

    form = CityForm(request.GET or None)
    yandex = ''
    openweather = ''
    average = ''
    last_update_time = ''

    if request.method == 'GET' and form.is_valid():

        city = form.cleaned_data['city_name']

        response = last_update.last_update_temperature(city)
        if response.status_code == 404:
            return HttpResponse(render(request, 'frontend/error404.html', locals()), status='404')
        if response.status_code == 500:
            return HttpResponse(render(request, 'frontend/error500.html', locals()), status='500')

        response = json.loads(response.content.decode('utf-8'))
        yandex_value = response['Temperature']['Yandex']
        openweather_value = response['Temperature']['Open weather']

        #values for GET
        yandex = 'Yandex: {}'.format(yandex_value)
        openweather = 'OpenWeatherMap: {}'.format(openweather_value)
        average = 'Average: {}'.format((float(yandex_value) + float(openweather_value))/2)
        last_update_time = 'Last update: {}'.format(response['Time'][:19])
    return HttpResponse(render(request, 'frontend/new-index.html', locals() ), status = '200')

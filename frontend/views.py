from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from . import database
import json

#вернуть назад, эксперимент с httpresponse
def index(request):
    # data = {
    #     'Error': 404,
    #     'Why': 'Bad request'
    # }
    #
    # data1 = json.dumps(data)
    # response = HttpResponse(data1)
    # response.status_code = 404
    # form = CityForm(request.POST or None)
    # print(dir(weather))
    form = CityForm(request.POST or None)
    results = ''
    city = ''
    cities = []
    if request.method == 'POST' and form.is_valid():
        print(form.cleaned_data['city_name'])
        city = form.cleaned_data['city_name']
        cities.append(city)
        response = database.auto_update_function(cities)

        # # city_name = 'Weather in {}:'.format(city)
        # results = '{}: {}'.format(yandex.__name__.capitalize(), temp)
        return response
    return render(request, 'frontend/index.html', locals())
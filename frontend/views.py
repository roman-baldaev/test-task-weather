from django.shortcuts import render
from .forms import HistoryForm
from .weather import yandex


def index(request):
    form = HistoryForm(request.POST or None)
    results = ''
    city = ''
    if request.method == 'POST' and form.is_valid():
        print(form.cleaned_data['name'])
        city = form.cleaned_data['name']
        temp = yandex(city)
        city_name = 'Weather in {}:'.format(city)
        results = '{}: {}'.format(yandex.__name__, temp)
    return render(request, 'frontend/index.html', locals())
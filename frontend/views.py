from django.shortcuts import render


def index(request):

    place = 'New York'
    return render(request, 'frontend/index.html', locals())
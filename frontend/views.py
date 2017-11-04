from django.shortcuts import render
from .forms import HistoryForm

def index(request):


    form = HistoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        print(request.POST)
        print(form.cleaned_data)
    return render(request, 'frontend/index.html', locals())
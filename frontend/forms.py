from django import  forms
from .models import *


class CityForm(forms.ModelForm):

    class Meta:
        model = City
        exclude = []


class HistoryForm(forms.ModelForm):

    class Meta:
        model = History
        exclude = []
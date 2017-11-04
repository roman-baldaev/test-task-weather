from django import  forms
from .models import *

class HistoryForm(forms.ModelForm):

    class Meta:
        model = History
        exclude = ['date', 'value']
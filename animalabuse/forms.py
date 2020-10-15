from django.forms import ModelForm
from .models import animalabuse
from django import forms



class SubmitForm(ModelForm):
    class Meta:
        model = animalabuse
        exclude = ('Address', 'DOB','expirationdate','image')



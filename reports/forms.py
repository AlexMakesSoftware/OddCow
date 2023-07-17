from django import forms
from django.core.validators import MaxLengthValidator

class IncidentSearchForm(forms.Form):    
    incident_number = forms.CharField(max_length=8, validators=[MaxLengthValidator(8)],
                                       required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
from django import forms
from django.core.validators import MaxLengthValidator
from .models import IncidentReport

class IncidentSearchForm(forms.Form):    
    incident_number = forms.CharField(max_length=8, validators=[MaxLengthValidator(8)],
                                       required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id':"incident_num"}))

class ReportCreateForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = ('start_date', 'end_date', 'status')
        widgets = {
            'start_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'end_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=IncidentReport.STATUS_CHOICES)
        }
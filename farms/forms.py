from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator

class FarmSearchForm(forms.Form):    
    county = forms.CharField(max_length=2, validators=[MaxLengthValidator(2)], required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    parish = forms.CharField(max_length=3, validators=[MaxLengthValidator(3)], required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    holding_number = forms.CharField(max_length=5, validators=[MaxLengthValidator(5)], required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

#TODO: https://www.youtube.com/watch?v=6-XXvUENY_8
#https://docs.djangoproject.com/en/4.2/topics/forms/

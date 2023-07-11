from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator

class FarmSearchForm(forms.Form):
    county = forms.CharField(max_length=2, validators=[MaxLengthValidator(2)], required=False)
    parish = forms.CharField(max_length=3, validators=[MaxLengthValidator(3)], required=False)
    holding_number = forms.CharField(max_length=5, validators=[MaxLengthValidator(5)], required=False)

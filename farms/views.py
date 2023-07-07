from django.shortcuts import render

from .models import Farm

def farms_index(request):
    data = Farm.objects.using('legacy').all()[:20]
    return render(request, "farms/farms.html", {'farms': data})

from django.shortcuts import render

from .models import IncidentReport

# Create your views here.
def reports_index(request):
    reports = IncidentReport.objects.all()
    return render(request, "reports/reports.html", {'reports':reports})
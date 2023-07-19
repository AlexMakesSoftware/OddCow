from django.shortcuts import render

from farms.models import Farm
from reports.models import IncidentReport


def dash(request):
    report_search = request.POST.get('report_search')

    if(report_search):
        reports_data = IncidentReport.objects.filter(incident_number=report_search)[:20]
    else:        
        reports_data = IncidentReport.objects.all()

    return render(request, "index.html", { 'reports':reports_data})
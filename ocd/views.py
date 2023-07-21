from django.shortcuts import render

from farms.models import Farm
from reports.models import IncidentReport


def home(request):
    report_search = request.POST.get('report_search')

    if(report_search):
        reports_data = IncidentReport.objects.filter(incident_number=report_search)[:20]
    else:        
        reports_data = IncidentReport.objects.all()

    return render(request, "index.html", { 'reports':reports_data})


def server_error(request):
    return render(request, 'errors/500.html')

def not_found(request, exception):
    return render(request, 'errors/404.html')

def permission_denied(request, exception):
    return render(request, 'errors/403.html')

def bad_request(request, exception):
    return render(request, 'errors/400.html')
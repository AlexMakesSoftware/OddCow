from django.shortcuts import render

from farms.models import Farm
from reports.models import IncidentReport


def home(request):
    reports_data = IncidentReport.objects.all().filter(assigned_to=request.user)
    return render(request, "index.html", { 'reports':reports_data })


def server_error(request):
    return render(request, 'errors/500.html')

def not_found(request, exception):
    return render(request, 'errors/404.html')

# def permission_denied(request, exception): #Not sure I want that.
#     return render(request, 'errors/403.html')

def bad_request(request, exception):
    return render(request, 'errors/400.html')
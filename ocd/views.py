from django.shortcuts import render

from farms.models import Farm
from reports.models import IncidentReport

def home(request):
    # Rather than duplicate the lookup logic, I probably want to put this in one place 
    # In the apps themselves and then just reference it here, getting dicts as a result and
    # passing them on.
    # I still need to figure out how to paginate and do searches.
    farms_data = Farm.objects.using('legacy').all()[:20]
    reports_data = reports = IncidentReport.objects.all()    
    return render(request, "index.html", { 'farms': farms_data, 'reports':reports})
from django.shortcuts import render

from farms.models import Farm
from reports.models import IncidentReport

#Dashboard view
def dash(request):
    # Rather than duplicate the lookup logic, I probably want to put this in one place 
    # In the apps themselves and then just reference it here, getting dicts as a result and
    # passing them on.
    # I still need to figure out how to paginate and do searches.


    farm_search = request.POST.get('farm_search')
    report_search = request.POST.get('report_search')

    if(farm_search):        
        farms_data = Farm.objects.filter(holding_number=farm_search)[:20]
    else:
        farms_data = Farm.objects.using('legacy').all()[:20]

    if(report_search):
        reports_data = IncidentReport.objects.filter(incident_number=report_search)[:20]
    else:        
        reports_data = IncidentReport.objects.all()

    return render(request, "index.html", { 'farms': farms_data, 'reports':reports_data})
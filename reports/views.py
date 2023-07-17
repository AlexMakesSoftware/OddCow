from django.shortcuts import render
from .forms import IncidentSearchForm
from .models import IncidentReport
from django.core.paginator import Paginator
from .models import IncidentReport

# Create your views here.
def reports_index(request):
    reports = IncidentReport.objects.all()
    return render(request, "reports/reports.html", {'reports':reports})


def reports_search(request):
    pagination_size = 20  # Default value
    reports = IncidentReport.objects.all()

    if request.method == "GET":
        form = IncidentSearchForm(request.GET)
        if form.is_valid():

            #Filter by holding.            
            if form.cleaned_data.get('incident_number') != '':           
                reports = reports.filter(
                    incident_number__icontains=form.cleaned_data['incident_number'])            
    else:
        form = IncidentSearchForm()

    # Pagination
    p = Paginator(reports, pagination_size)  # Display 20 records per page
    page_number = request.GET.get('page')  # Get the current page number from the request's GET parameters    
    
    page_obj = p.get_page(page_number)  # Get the Page object for the current page number    

    context = {
        'form': form,
        'report_records': page_obj
    }
    return render(request, 'reports/search_reports.html', context)
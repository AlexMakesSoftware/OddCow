from django.shortcuts import render
from .forms import FarmSearchForm
from .models import Farm
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from reports.models import IncidentReport

def farms_search(request):
    pagination_size = 20  # Default value
    farm_records = Farm.objects.using('legacy').all()

    if request.method == "GET":
        form = FarmSearchForm(request.GET)
        if form.is_valid():
            holding_number = form.cleaned_data.get('holding_number')
            county = form.cleaned_data.get('county')
            parish = form.cleaned_data.get('parish')

            farm_records = Farm.search(
                holding_number=holding_number,
                county=county,
                parish=parish
            )
        else:
            farm_records = Farm.objects.using('legacy').all()
            form = FarmSearchForm()
    else:
        farm_records = Farm.objects.using('legacy').all()
        form = FarmSearchForm()

    # Pagination
    p = Paginator(farm_records, pagination_size)  # Display 20 records per page
    page_number = request.GET.get('page')  # Get the current page number from the request's GET parameters    
    page_obj = p.get_page(page_number)  # Get the Page object for the current page number

    context = {
        'form': form,
        'farm_records': page_obj
    }
    return render(request, 'farms/search_farms.html', context)



class FarmView(TemplateView):
    template_name = "farms/Farm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farm_id = self.kwargs.get('farm_id')  # Retrieve the farm ID from the URL
        farm = Farm.objects.using('legacy').get(id=farm_id)  # Retrieve the farm object using the ID
        context['farm'] = farm  # Add the farm object to the context
        
        reports = IncidentReport.get_reports_by_cph(county = farm.county, parish = farm.parish, holding_number = farm.holding_number)
        context['reports'] = reports

        return context
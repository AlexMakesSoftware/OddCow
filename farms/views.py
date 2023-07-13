from django.shortcuts import render
from .forms import FarmSearchForm
from .models import Farm
from django.core.paginator import Paginator


def farms_index(request):
    data = Farm.objects.using('legacy').all()[:20]
    return render(request, "farms/farms.html", {'farms': data})


def farms_search(request):
    pagination_size = 20  # Default value
    farm_records = Farm.objects.using('legacy').all()

    if request.method == "GET":
        form = FarmSearchForm(request.GET)
        if form.is_valid():

            #Filter by holding.            
            if form.cleaned_data.get('holding_number') != '':           
                farm_records = farm_records.filter(
                    holding_number__icontains=form.cleaned_data['holding_number'])
            
            #Filter by county
            county_val = form.cleaned_data.get('county')
            if county_val != '':
                try:
                    county_int = int(county_val)
                    farm_records = farm_records.filter(
                        county=form.cleaned_data['county'])
                except ValueError:
                    print("Ooops!")
                    pass
                    #ignore it.
            
            #Filter by parish
            if form.cleaned_data.get('parish') != '':
                farm_records = farm_records.filter(
                    parish__icontains=form.cleaned_data['parish'])
    else:
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
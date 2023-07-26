from typing import Any, Dict
from django.shortcuts import render
from .forms import IncidentSearchForm, ObservationCreateForm
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView
from .models import IncidentReport, FarmCopy, OwnerCopy
from farms.models import Farm as LegacyFarmData
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import DetailView
from .forms import ReportCreateForm
from django.urls import reverse


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



class ReportDetailView(DetailView):
    model = IncidentReport
    template_name = 'reports/report_detail.html'
    observation_form_class = ObservationCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.observation_form_class()
        return context

    def post(self, request, *args, **kwargs):
        incident_report = self.get_object()
        print("DEBUG:", incident_report)
        form = self.observation_form_class(request.POST)
        if form.is_valid():
            # Create a new Observation instance but don't save it yet
            observation = form.save(commit=False)                
            # Associate the observation with the IncidentReport
            observation.incident = incident_report
            observation.user = self.request.user            
            # Save the observation
            observation.save()
            messages.success(self.request, "Observation added successfully.")
            return redirect('report_detail', pk=incident_report.pk)
        
        # If the form is not valid, re-render the template with the form errors
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class ReportCreateView(CreateView):
    model = IncidentReport    
    form_class = ReportCreateForm
    template_name = 'reports/report_create.html'
    
    def form_valid(self, form):
        farm_id = self.kwargs.get('farm_id')

        try:
            farm = LegacyFarmData.objects.using('legacy').get(id=farm_id)
        except LegacyFarmData.DoesNotExist:
            raise ObjectDoesNotExist(f"Legacy farm data with the id {farm_id} cannot be found.")

        with transaction.atomic():
            #TODO: I need a 'find_or_create_from_legacy' method for these that returns the farm.
            farm_copy = FarmCopy.find_or_copy_from(farm)
            
            # Create an Incident linked to the copied data
            incident = IncidentReport.objects.create(
                farm=farm_copy,
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
                status=form.cleaned_data['status'],
                created_by=self.request.user,
                assigned_to=self.request.user
            )            
        
        # return super().form_valid(form) we don't want to do this because it will try to save the form for us.
        messages.success(self.request, "Report created successfully.")
        return redirect('report_detail', pk=incident.pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farm_id = self.kwargs.get('farm_id')
        farm = LegacyFarmData.objects.using('legacy').get(id=farm_id)
        context['farm'] = farm
        return context
from django.views.generic.edit import CreateView
from .models import IncidentReport, FarmCopy, OwnerCopy
from farms.models import Farm as LegacyFarmData
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import DetailView


class ReportDetailView(DetailView):
    model = IncidentReport
    template_name = 'reports/report_detail.html'


class ReportCreateView(CreateView):
    model = IncidentReport
    fields = ['start_date','end_date','status']
    template_name = 'reports/report_create.html'
    
    def form_valid(self, form):
        farm_id = self.kwargs.get('farm_id')

        try:
            farm = LegacyFarmData.objects.using('legacy').get(id=farm_id)
        except LegacyFarmData.DoesNotExist:
            raise ObjectDoesNotExist(f"Legacy farm data with the id {farm_id} cannot be found.")

        with transaction.atomic():
            #duplicate the legacy data.
            owner_copy = OwnerCopy.objects.create(
                first_name = farm.owner.first_name,
                last_name = farm.owner.last_name,
                email = farm.owner.email,
                phone = farm.owner.phone
            )
            
            farm_copy = FarmCopy.objects.create(
                county = farm.county,
                parish = farm.parish,
                holding_number = farm.holding_number,
                address_line1 = farm.address_line1,
                address_line2 = farm.address_line2,
                city = farm.city,
                postcode = farm.postcode,
                farm_name = farm.farm_name,
                owner = owner_copy
            )
            
            # Create an Incident linked to the copied data
            incident = IncidentReport.objects.create(
                farm=farm_copy,
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
                status=form.cleaned_data['status']
            )            
        
        # return super().form_valid(form) we don't want to do this because it will try to save the form for us.
        messages.success(self.request, "Report created successfully.")
        return redirect('report_detail', pk=incident.pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farm_id = self.kwargs.get('farm_id')
        farm = LegacyFarmData.objects.using('legacy').get(id=farm_id)
        context['farm'] = farm
        print("got ",farm_id)
        return context
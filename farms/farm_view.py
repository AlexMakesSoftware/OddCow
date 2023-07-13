from django.views.generic.base import TemplateView
from .models import Farm

class FarmView(TemplateView):
    template_name = "farms/Farm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farm_id = self.kwargs.get('farm_id')  # Retrieve the farm ID from the URL
        farm = Farm.objects.using('legacy').get(id=farm_id)  # Retrieve the farm object using the ID
        context['farm'] = farm  # Add the farm object to the context
        return context
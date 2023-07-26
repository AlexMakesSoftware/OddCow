from django.contrib import admin
from django.urls import reverse
from .models import FarmCopy, OwnerCopy, IncidentReport, Observation


class ReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
class FarmAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    pass

class OwnerAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    pass

class ObservationsAdmin(admin.TabularInline):
    model = Observation
    extra = 1

class IncidentReportAdmin(admin.ModelAdmin):    
    inlines = [ObservationsAdmin]

admin.site.register(OwnerCopy, OwnerAdmin)
admin.site.register(FarmCopy, FarmAdmin)
admin.site.register(IncidentReport, IncidentReportAdmin)




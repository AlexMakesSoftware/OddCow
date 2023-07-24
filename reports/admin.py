from django.contrib import admin
from django.urls import reverse
from .models import FarmCopy, OwnerCopy, IncidentReport


class ReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
class FarmAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    pass

class OwnerAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    pass

class IncidentReportAdmin(admin.ModelAdmin):    
    pass

class CustomAdminSite(admin.AdminSite):
    def get_logout_url(self):
        return reverse('logout')

admin.site.register(OwnerCopy, OwnerAdmin)
admin.site.register(FarmCopy, FarmAdmin)
admin.site.register(IncidentReport, IncidentReportAdmin)

# Redirects logout for the admin to the login page.
admin.site = CustomAdminSite()
admin.sites.site = admin.site
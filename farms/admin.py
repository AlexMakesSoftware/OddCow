from django.contrib import admin

from .models import *

class FarmInline(admin.StackedInline):    
    model = Farm
    extra = 0    

class OwnerAdmin(admin.ModelAdmin):
    inlines = [FarmInline]
    list_per_page = 20

class FarmsAdmin(admin.ModelAdmin):
    model=Farm
    list_per_page = 20

admin.site.register(Owner, OwnerAdmin)
admin.site.register(Farm, FarmsAdmin)



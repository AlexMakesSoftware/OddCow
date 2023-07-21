from django.urls import path
from . import views
from .views import FarmView


urlpatterns = [    
    path('search/', views.farms_search, name='search_farm_records'),    
    path('<int:farm_id>/', FarmView.as_view(), name="farm_view")
]

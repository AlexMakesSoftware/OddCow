from django.urls import path
from .farm_view import FarmView
from . import views


urlpatterns = [
    path('', views.farms_index, name='index'),
    path('search/', views.farms_search, name='search_farm_records'),
    path('<int:farm_id>/', FarmView.as_view(), name="farm_view")
]

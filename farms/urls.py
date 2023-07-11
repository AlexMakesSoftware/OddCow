from django.urls import path
from . import views

urlpatterns = [
    path('', views.farms_index, name='index'),
    path('search/', views.farms_search, name='search_farm_records'),
]

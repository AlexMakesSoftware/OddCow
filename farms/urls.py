from django.urls import path
from . import views

urlpatterns = [
    path('', views.farms_index, name='index'),
]

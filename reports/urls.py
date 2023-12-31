from django.urls import path
from . import views
from .views import ReportCreateView, ReportDetailView


urlpatterns = [
    path('reports/create/<int:farm_id>', ReportCreateView.as_view(), name='report-create'),
    path('report/<int:pk>', ReportDetailView.as_view(), name="report_detail"),
    path('search/', views.reports_search, name='search_report_records')    
]

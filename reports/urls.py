from django.urls import path
from . import views
from .report_view import ReportCreateView
from .report_view import ReportDetailView

urlpatterns = [
    path('', views.reports_index, name='index'),
    path('reports/create/<int:farm_id>', ReportCreateView.as_view(), name='report-create'),
    path('report/<int:pk>', ReportDetailView.as_view(), name="report_detail"),
    path('search/', views.reports_search, name='search_report_records')    
]

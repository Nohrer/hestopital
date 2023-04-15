from django.urls import path
from dashboard.views import pa_dashboard ,doctor_dashboard,receptionist_dashboard,report_details,report_details_forDoc
from . import views

app_name='dashboard'

urlpatterns = [
    path('doctor_dashboard/', doctor_dashboard,name="doctor_dashboard"),
    path('pa_dashboard/', pa_dashboard, name='pa_dashboard'),
    path('receptionist_dashboard/', receptionist_dashboard, name='receptionist_dashboard'),
    path('report/<int:report_id>/', report_details, name='report_details'),
    path('report_details_forDoc/<int:pk>/', report_details_forDoc, name='report_details_forDoc'),

]

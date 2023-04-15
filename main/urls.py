from django.contrib import admin
from django.urls import path,include
from main import views
from .views import patient_dashboard,appointment_detail,createAppointementS

app_name='main'


urlpatterns = [
      path("",views.home, name="home"), 

      path('accounts/', include('accounts.urls', namespace="accounts")),

      
      path('search/', views.search, name='search'),
      path('detail/<int:result_id>/', views.detail, name='detail'),
      path('detail_doc/<int:result_id>/', views.detail, name='detail'),
      path('detail_doc_rc/<int:result_id>/', views.detail_rc, name='detail_rc'),


      
      path('create_appointement/', views.create_appointement, name='create_appointement'),
      path('appointement/<int:patient_id>/', createAppointementS, name='createAppointementS'),
      path('appointment_list/', views.appointment_list, name='appointment_list'),
      path('search_appointment/', views.search_appointment, name='search_appointment'),


      path('request_appointment/', views.request_appointment, name='request_appointment'),
      path('requested_appointments/', views.requested_appointments, name='requested_appointments'),
      path('appointment/requests/', views.appointment_requests, name='appointment_requests'),
      path('appointment/<int:appointment_id>/', appointment_detail, name='appointment_detail'),
      path('doctor_appointments_for_date/', views.doctor_patients_for_day, name='doctor_patients_for_day'),
      path('dashboard/patient/', patient_dashboard, name='patient_dashboard'),

      path('report_creation/<int:patient_id>/', views.create_repport, name='create_repport'),
      path('report_update/<int:report_id>/', views.update_repport, name='update_repport'),


]

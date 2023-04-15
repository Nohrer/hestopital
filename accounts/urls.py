from django.urls import path
from .import views

app_name='accounts'

urlpatterns=[
    path('',views.login_choices,name='login_choices'),
    path('patient_registration/',views.patient_registration,name='patient_registration'),
    path('doctor_registration/',views.doctor_registration,name='doctor_registration'),
    path('receptionist_registration/',views.receptionist_registration,name='receptionist_registration'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('patient_login/', views.patient_login, name='patient_login'),
    path('receptionist_login/', views.receptionist_login, name='receptionist_login'),
    path('logout_user/', views.logout_user, name='logout_user'),

]

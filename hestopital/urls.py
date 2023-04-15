"""hestopital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as v
from dashboard.views import pa_dashboard ,doctor_dashboard,receptionist_dashboard,report_details,report_details_forDoc

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("main.urls")),
    path('pa_dashboard/', pa_dashboard, name='pa_dashboard'),
    path('doctor_dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('receptionist_dashboard/', receptionist_dashboard, name='receptionist_dashboard'),
    path('report/<int:report_id>/', report_details, name='report_details'),
    path('report_details_forDoc/<int:pk>/', report_details_forDoc, name='report_details_forDoc'),


]

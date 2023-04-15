import json
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.models import Patient,User,Doctor,Receptionist
from main.models import MedicalRecord,Repport,Appointment
from django.core.paginator import Paginator

# Create your views here.


@login_required
@user_passes_test(lambda user: user.is_patient)
def pa_dashboard(request):
    patient = request.user.patient
    medical_record = MedicalRecord.objects.get(patient=request.user.patient)
    reports = Repport.objects.filter(medical_record=medical_record).order_by('-date')
    context={
        'patient':patient,
        'reports':reports

    }
    return render(request, 'pa_dashboard.html',context)


@login_required
@user_passes_test(lambda user: user.is_patient)
def report_details(request, report_id):
    patient = request.user.patient
   
    report = Repport.objects.get(id=report_id)
   
    context = {
        'report': report,
        'patient': patient
    }
    return render(request, 'report_details.html', context)


@login_required
@user_passes_test(lambda user: user.is_doctor)
def doctor_dashboard(request):
    doctor = Doctor.objects.get(user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor)
    patients = set(appointment.patient for appointment in appointments)
    paginator = Paginator(list(patients), 8)  # Convert set to list before paginating
    page_number = request.GET.get('page')
    patients = paginator.get_page(page_number)
    patients = list(patients)
    patients.sort(key=lambda p: p.firstName)

    context = {
        'doctor': doctor,
        'patients': patients,
    }
    return render(request, 'doctor_dashboard.html', context)

@login_required
@user_passes_test(lambda user: user.is_receptionist)
def receptionist_dashboard(request):
    patients = Patient.objects.all()
    receptionist = request.user.receptionist
    paginator = Paginator(patients, 8)
    page = request.GET.get('page')
    patients = paginator.get_page(page)
    patients = list(patients)
    patients.sort(key=lambda p: p.firstName)

    context={
        "patients":patients,
        "receptionist":receptionist
    }
    return render(request,'receptionist_dashboard.html',context)

def report_details_forDoc(request, pk):
    doctor = Doctor.objects.get(user=request.user)

    report = get_object_or_404(Repport, id=pk)
    context = {'report': report,'doctor':doctor}
    return render(request, 'report_details_doc.html', context)



from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from.models import Appointment,MedicalRecord,Repport
from accounts.models import Patient,Doctor,Receptionist
from .forms import AppointmentRequestForm,AppointmentRescheduleForm,AppointementForm,AppointmentResponseForm,Appointment,RepportForm
from django.contrib import messages
from django.db.models import Q
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.core.paginator import Paginator


# Create your views here.

def home(response):
    return render(response,"main/home.html",{})

# APPOINTEMENT MANAGMENT
@login_required
@user_passes_test(lambda user: user.is_doctor)
def create_appointement(request):
    my_form = AppointementForm()
    doctor = Doctor.objects.get(user=request.user)
    
    if request.method == "POST":
        my_form = AppointementForm(request.POST)
        if my_form.is_valid():
            appointment = Appointment(**my_form.cleaned_data)
            appointment.doctor=doctor
            appointment.save() 
            return redirect('doctor_dashboard') 

    else:
        initial_data = {'doctor': doctor}
        my_form = AppointementForm(initial=initial_data)
        
    context1 = {
        'form': my_form,
        'doctor': doctor
    }

    return render(request, "main/create_appointement_doctor.html/", context1)



@login_required
@user_passes_test(lambda user: user.is_receptionist)
def createAppointementS(request,patient_id):
    my_form = AppointementForm()
    patient = get_object_or_404(Patient, pk=patient_id)
    receptionist=Receptionist.objects.get(user=request.user)

    if request.method == "POST":
        my_form=AppointementForm(request.POST)
        if my_form.is_valid():
            Appointment.objects.create(**my_form.cleaned_data)
            my_form = AppointementForm()
            return redirect('receptionist_dashboard') 
    else:
        initial_data = {'patient': patient}
        my_form = AppointementForm(initial=initial_data)
    
    context2 = {
        'form': my_form,
        'receptionist': receptionist
    }

    return render(request, "main/create_appointement_receptionist.html/", context2)

@login_required
@user_passes_test(lambda user: user.is_receptionist)
def appointment_list(request):
    appointment_list = Appointment.objects.all().order_by('-date')
    receptionist = Receptionist.objects.get(user=request.user)

    # Pagination
    paginator = Paginator(appointment_list, 8)
    page = request.GET.get('page')
    appointments = paginator.get_page(page)

    return render(request, 'main/appointment_list.html', {'appointments': appointments, 'receptionist': receptionist})
@login_required
@user_passes_test(lambda user: user.is_patient)
def request_appointment(request):
    patient = Patient.objects.get(user=request.user)
    if request.method == 'POST':
        form = AppointmentRequestForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            # Ajouter une vérification pour empêcher la sélection d'une date passée
            if appointment.date < timezone.localdate():
                messages.error(request, 'You can\'t select a passed date')
                return render(request, 'main/request_appointment.html', {'form': form, 'patient': patient})
            appointment.patient = request.user.patient
            appointment.save()
            return redirect('pa_dashboard')
    else:
        form = AppointmentRequestForm()
    return render(request, 'main/request_appointment.html', {'form': form,'patient':patient})


@login_required
@user_passes_test(lambda user: user.is_patient)
def requested_appointments(request):
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=request.user.patient, status='requested').order_by('-date')
    

    return render(request, 'main/requested_appointments.html', {'appointments': appointments,'patient':patient})

# REQUEST APPOINTEMENT

@login_required
@user_passes_test(lambda user: user.is_receptionist)
def appointment_requests(request):
    receptionist = Receptionist.objects.get(user=request.user)
    appointments = Appointment.objects.filter(status='requested').order_by('-date')
    paginator = Paginator(appointments, 8)
    page = request.GET.get('page')
    appointments = paginator.get_page(page)
    return render(request, 'main/appointment_requests.html', {'appointments': appointments,'receptionist':receptionist})


from datetime import time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Appointment
from .forms import AppointmentStatusForm
from datetime import date
from datetime import  timedelta,datetime

def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    # Utiliser la date de l'appointment comme date sélectionnée par défaut si aucune date n'est fournie
    selected_date = request.GET.get('selected_date') or appointment.date.strftime('%Y-%m-%d')

    # Rechercher les rendez-vous du médecin pour la date sélectionnée
    doctor_appointments = Appointment.objects.filter(doctor=appointment.doctor, date=selected_date, status__in=['proposed', 'requested','confirmed'])

    if request.method == 'POST':
        form = AppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            updated_appointment = form.save(commit=False)
            status = updated_appointment.status

            if status == 'confirmed' and not updated_appointment.time:
                messages.error(request, "Enter a valide hour for the accepted appointment.")
                return redirect('main:appointment_detail', appointment_id=appointment_id)

            if status == 'cancelled' and not updated_appointment.cause:
                messages.error(request, "Enter a valide cause for rejecting this request")
                return redirect('main:appointment_detail', appointment_id=appointment_id)

            if status == 'proposed' and (not updated_appointment.time or not updated_appointment.date):
                messages.error(request, "Enter a valide hour and date  for the proposed appointment.")
                return redirect('main:appointment_detail', appointment_id=appointment_id)

            # Vérifier si l'heure de rendez-vous est comprise entre 8h30 et 18h00
            if updated_appointment.time is not None:
                min_time = time(hour=8, minute=30)
                max_time = time(hour=18, minute=0)
                if updated_appointment.time < min_time or updated_appointment.time > max_time:
                    messages.error(request, "appointments hours need to be between 8h30-18h00.")
                    return redirect('main:appointment_detail', appointment_id=appointment_id)

            # Vérifier s'il y a des conflits de rendez-vous dans un intervalle de 7 minutes
            if status == 'proposed':
                # Vérifier si la date est passée
                if updated_appointment.date < date.today():
                    messages.error(request, "You can't accept an appointment in passed date.")
                    return redirect('main:appointment_detail', appointment_id=appointment_id)
                if updated_appointment.time is not None:
                    appointment_time = updated_appointment.time
                    appointment_date = updated_appointment.date
                    doctor_appointments_for_date = doctor_appointments.filter(time__isnull=False).values_list('time', flat=True)
                    if appointment_time in doctor_appointments_for_date:
                        messages.error(request, "Appointment is already booked for this time,try another one.")
                        return redirect('main:appointment_detail', appointment_id=appointment_id)

            if status == 'confirmed':
                # Vérifier si la date est passée
                if updated_appointment.date < date.today():
                    messages.error(request, "You can't propose or accepte an appontment  in passed date.")
                    return redirect('main:appointment_detail', appointment_id=appointment_id)
                if updated_appointment.time is not None:
                    appointment_time = updated_appointment.time
                    appointment_date = updated_appointment.date
                    doctor_appointments_for_date = doctor_appointments.filter(time__isnull=False).values_list('time', flat=True)
                    if appointment_time in doctor_appointments_for_date:
                        messages.error(request, "Appointment is already booked for this time,try another one.")
                        return redirect('main:appointment_detail', appointment_id=appointment_id)


            updated_appointment.save()
            messages.success(request, f"Appointment has been updated.")
            try:
                url = reverse('main:appointment_requests')
            except:
                messages.error(request, "ERROR:try again")
                return redirect('main:appointment_detail', appointment_id=appointment_id)

            return redirect(url)

    else:
        form = AppointmentStatusForm(instance=appointment)

    receptionist = Receptionist.objects.get(user=request.user)

    context = {
        'appointment': appointment,
        'doctor_appointments': doctor_appointments,
        'form': form,
        'selected_date': selected_date,
        'receptionist':receptionist,
    }

    return render(request, 'main/appointment_detail.html', context)


@login_required
@user_passes_test(lambda user: user.is_doctor)
def doctor_patients_for_day(request):
    # Get the date from the request or use today's date
    date_str = request.GET.get("date")
    doctor = Doctor.objects.get(user=request.user)

    if not date_str:
        date = timezone.now().date()
    else:
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()

    # Get all appointments for the logged-in doctor for the given date
    appointments = Appointment.objects.filter(doctor=request.user.doctor, date=date).exclude(status__in=('cancelled','requested','proposed')).filter(status='confirmed')

    # Get the list of patients for the appointments
    patients = [appointment.patient for appointment in appointments]

    context = {
        'date': date,
        'patients': patients,
        'doctor': doctor,
    }

    return render(request, 'main/doctor_patients_for_day.html', context)


@user_passes_test(lambda user: user.is_doctor)
@login_required
def repport_list(request):
    doctor = request.user.doctor
    repports = Repport.objects.filter(doctor=doctor)
    context = {
        'repports': repports,
    }
    return render(request, 'main/repport_list.html', context)

from django.shortcuts import redirect, render
from .models import Appointment

@login_required
@user_passes_test(lambda user: user.is_patient)

def patient_dashboard(request):
    patient = request.user.patient
    accepted_appointments = Appointment.objects.filter(patient=request.user.patient, status='confirmed').order_by('-date')
    new_proposals = Appointment.objects.filter(patient=request.user.patient, status='proposed').order_by('-date')
    cancelled_appointments = Appointment.objects.filter(patient=request.user.patient, status='cancelled').order_by('-date')

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        action = request.POST.get('action')

        if appointment_id and action:
            try:
                appointment = Appointment.objects.get(id=appointment_id, patient=request.user.patient)
                if action == 'accept':
                    appointment.status = 'confirmed'
                elif action == 'cancel':
                    appointment.status = 'cancelled'
                appointment.save()
            except Appointment.DoesNotExist:
                pass

        return redirect('main:patient_dashboard')  # redirige l'utilisateur vers la page du tableau de bord du patient après chaque changement de statut

    return render(request, 'main/patient_dashboard.html', {
        'accepted_appointments': accepted_appointments,
        'new_proposals': new_proposals,
        'cancelled_appointments': cancelled_appointments,
        'patient': patient,
    })
@login_required
@user_passes_test(lambda user: user.is_doctor or user.is_receptionist)
def search(request):
    query = request.GET.get('q')
    doctor=None
    if request.user.is_doctor:
        doctor = Doctor.objects.get(user=request.user)
        results = Patient.objects.all().filter(appointment__doctor=doctor,appointment__status='confirmed').filter(
            Q(cin__icontains=query) 
            | Q(firstName__icontains=query) 
            | Q(lastName__icontains=query) 
            | Q(phoneNumber__icontains=query)
            )
        return render(request, 'main/search.html', {'results': results,'doctor':doctor})
    else:
        receptionist = Receptionist.objects.get(user=request.user)
        results = Patient.objects.all().filter(
            Q(cin__icontains=query) 
            | Q(firstName__icontains=query) 
            | Q(lastName__icontains=query) 
            | Q(phoneNumber__icontains=query)
            )
        return render(request, 'main/searchrecep.html', {'results': results,'doctor':receptionist})

#SEARCH FOR APPOINTMENTS
@login_required
@user_passes_test(lambda user: user.is_receptionist)
def search_appointment(request):
    query = request.GET.get('q')
    receptionist = Receptionist.objects.get(user=request.user)
    results = Appointment.objects.filter(  
        Q(patient__firstName__icontains=query) 
        | Q(patient__lastName__icontains=query)
        | Q(doctor__firstName__icontains=query)
        | Q(doctor__lastName__icontains=query)
        | Q(date__icontains=query) 
        | Q(time__icontains=query)
        | Q(complete__icontains=query)
        | Q(status__icontains=query)
    )
    return render(request, 'main/search_appointment.html', {'results': results, 'receptionist': receptionist})


@login_required
@user_passes_test(lambda user: user.is_doctor)
def detail(request, result_id):
    result = get_object_or_404(Patient, pk=result_id)
    doctor = Doctor.objects.get(user=request.user)
    medical_records = MedicalRecord.objects.filter(repport__doctor=doctor, patient=result)
    repport = Repport.objects.filter(medical_record__in=medical_records).order_by('-date')

    return render(request, 'main/patient_detail.html', {
        'result': result,
        'doctor': doctor,
        'repport': repport,
    })

@login_required
@user_passes_test(lambda user: user.is_receptionist)
def detail_rc(request, result_id):
    result = get_object_or_404(Patient, pk=result_id)
    receptionist = Receptionist.objects.get(user=request.user)

    return render(request, 'main/patient_detail_rc.html', {'result': result,'receptionist':receptionist})

#REPPORTS
@login_required
@user_passes_test(lambda user: user.is_doctor)
def create_repport(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    medical_record = MedicalRecord.objects.get(patient=patient)
    doctor = Doctor.objects.get(user=request.user)
    doctorinfo = request.user.doctor
    
    if request.method == 'POST':
        form = RepportForm(request.POST,initial={'medical_record': medical_record.pk, 'doctor': doctor.pk})
        if form.is_valid() :
            repport = form.save(commit=False)
            repport.medical_record = medical_record
            repport.doctor = doctor
            repport.save()
            return redirect('doctor_dashboard')
    else:

        form = RepportForm(initial={'medical_record': medical_record.pk, 'doctor': doctor.pk})
        
    return render(request, 'main/create_repport.html', {'form': form,'doctor': doctorinfo})



@login_required
@user_passes_test(lambda user: user.is_doctor)
def update_repport(request, report_id):
    repport = get_object_or_404(Repport, pk=report_id)
    doctor = Doctor.objects.get(user=request.user)
    medical_record = repport.medical_record


    if request.method == 'POST':
        form = RepportForm(request.POST, instance=repport)

        if form.is_valid():
            repport.doctor = doctor
            repport.medical_record=medical_record
            form.save()
            return redirect('doctor_dashboard')
    else:
        form = RepportForm(instance=repport)
        
    return render(request, 'main/update_repport.html', {'form': form, 'doctor': doctor})
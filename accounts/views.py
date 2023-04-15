from django.shortcuts import render , redirect
from django.contrib.auth import login,logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import PatientSignupForm,DoctorSignupForm,ReceptionistSignupForm,PatientAuthenticationForm,DoctorAuthenticationForm,ReceptionistAuthenticationForm
from django.contrib.auth.decorators import user_passes_test,login_required
from main.models import MedicalRecord


def is_superuser(user):
    return user.is_superuser
# ALL USER CREATION VIEWS
@login_required
def patient_registration(request):
    receptionist = request.user.receptionist

    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('receptionist_dashboard') 
    else:
        form = PatientSignupForm()
    return render(request, 'accounts/patient_registration.html', {'form': form,'receptionist':receptionist})

@login_required
@user_passes_test(is_superuser)
def doctor_registration(request):
    if request.method == 'POST':
        form = DoctorSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../../') 
    else:
        form = DoctorSignupForm()
    return render(request, 'accounts/doctor_registration.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def receptionist_registration(request):
    if request.method == 'POST':
        form = ReceptionistSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../../') 
    else:
        form = ReceptionistSignupForm()
    return render(request, 'accounts/receptionist_registration.html', {'form': form})


# ALL USER LOGIN
def login_choices(request):
    return render(request,'accounts/login_choices.html')


def doctor_login(request):
    if request.method == 'POST':
        form = DoctorAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_doctor:
                login(request, user)
                return redirect('doctor_dashboard')
            else:
                messages.error(request, 'You are not a doctor.')
        else:
            messages.error(request, 'Invalid login.')
    else:
        form = DoctorAuthenticationForm()
    return render(request, 'accounts/doctor_login.html', {'form': form})

def patient_login(request):
    if request.method == 'POST':
        form = PatientAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_patient:
                login(request, user)
                return redirect('pa_dashboard')
            else:
                messages.error(request, 'You are not a patient.')
        else:
            messages.error(request, 'Invalid login.')
    else:
        form = PatientAuthenticationForm()
    return render(request, 'accounts/patient_login.html', {'form': form})

def receptionist_login(request):
    if request.method == 'POST':
        form = ReceptionistAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_receptionist:
                login(request, user)
                return redirect('receptionist_dashboard')
            else:
                messages.error(request, 'You are not a receptionist.')
        else:
            messages.error(request, 'Invalid login.')
    else:
        form = ReceptionistAuthenticationForm()
    return render(request, 'accounts/receptionist_login.html', {'form': form})

# DASHBOARDS
@login_required

def logout_user(request):
    logout(request)
    return redirect('main:home')


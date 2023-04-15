from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
from .models import User,Patient,Doctor,Receptionist
from main.models import MedicalRecord
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin



class PatientSignupForm(UserCreationForm):

    firstName= forms.CharField(required=True)
    lastName= forms.CharField(required=True)
    phoneNumber= forms.CharField(required=True)
    cin = forms.CharField(required=True,max_length=8)
    birthDate = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self) :
        user = super().save(commit=False)
        user.is_patient = True
        user.save()
        patient = Patient.objects.create(user=user)
        patient.firstName = self.cleaned_data.get('firstName')
        patient.lastName = self.cleaned_data.get('lastName')
        patient.cin = self.cleaned_data.get('cin')
        patient.phoneNumber = self.cleaned_data.get('phoneNumber')
        patient.birthDate = self.cleaned_data.get('birthDate')
        patient.save()
        medical_record = MedicalRecord.objects.create(patient=patient)
        medical_record.save()
        return user
        

class DoctorSignupForm(UserCreationForm):
    firstName= forms.CharField(required=True)
    lastName= forms.CharField(required=True)
    phoneNumber= forms.CharField(required=True)
    cin = forms.CharField(required=True)
    birthDate = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))

    speciality = forms.CharField(required=True,max_length=100)
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self) :
        user = super().save(commit=False)
        user.is_patient = False
        user.is_doctor = True
        user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.firstName = self.cleaned_data.get('firstName')
        doctor.lastName = self.cleaned_data.get('lastName')
        doctor.cin = self.cleaned_data.get('cin')
        doctor.phoneNumber = self.cleaned_data.get('phoneNumber')
        doctor.speciality = self.cleaned_data.get('speciality')
        doctor.birthDate = self.cleaned_data.get('birthDate')
        doctor.save()
        return user



class ReceptionistSignupForm(UserCreationForm):
    firstName= forms.CharField(required=True)
    lastName= forms.CharField(required=True)
    phoneNumber= forms.CharField(required=True)
    cin = forms.CharField(max_length=8,required=True)
    birthDate = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self) :
        user = super().save(commit=False)
        user.is_patient = False
        user.is_doctor = False
        user.s_receptionist = True
        user.save()
        receptionist = Receptionist.objects.create(user=user)
        receptionist.firstName = self.cleaned_data.get('firstName')
        receptionist.lastName = self.cleaned_data.get('lastName')
        receptionist.cin = self.cleaned_data.get('cin')
        receptionist.phoneNumber = self.cleaned_data.get('phoneNumber')
        receptionist.birthDate = self.cleaned_data.get('birthDate')
        receptionist.save()
        return user
        




class DoctorAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Doctor
        fields = ['username', 'password']

class PatientAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Patient
        fields = ['username', 'password']

class ReceptionistAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Receptionist
        fields = ['username', 'password']
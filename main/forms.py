from django import forms
from .models import  Appointment,Doctor,Patient,Repport,MedicalRecord


class AppointmentRequestForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all())
    date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))


    class Meta:
        model = Appointment
        fields = ['doctor', 'date']
        
class AppointmentRescheduleForm(forms.ModelForm):
    cause = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'cause']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'min': '08:30', 'max': '18:00'}),
        }
        input_formats = {
            'time': ['%H:%M', '%I:%M%p'],
        }

from django import forms
from .models import Appointment

class AppointmentStatusForm(forms.ModelForm):
    cause = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': "Cause d'annulation"}))

    class Meta:
        model = Appointment
        fields = ('status', 'time', 'cause', 'date')
        widgets = {
            'status': forms.Select(choices=Appointment.STATUS_CHOICES),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
        input_formats = {
            'time': ('%H:%M',),
        }

class AppointementForm(forms.Form):
    patient =forms.ModelChoiceField( queryset=Patient.objects.all()
        ,widget=forms.Select(attrs={'size': 1}))
    doctor = forms.ModelChoiceField( queryset=Doctor.objects.all()
        ,widget=forms.Select(attrs={'size': 1,'id':'doctor'}),required=False)
    
    date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'placeholder':'hh:mm'}))
    status = forms.CharField(max_length=10,widget=forms.Select(choices=Appointment.STATUS_CHOICES),
    initial='Requested')
    

    class Meta:
        model = Appointment
        fields=[
            'patient',
            'doctor',
            'date',
            'time',
            'status'
            
        ]

class AppointmentResponseForm(forms.Form):
    appointment_id = forms.IntegerField(widget=forms.HiddenInput())
    response = forms.ChoiceField(choices=[('accept', 'Accept'), ('cancel', 'Cancel'), ('proposed', 'Proposed')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['response'].widget.attrs.update({'class': 'form-select'})

    def clean(self):
        cleaned_data = super().clean()
        appointment_id = cleaned_data.get('appointment_id')
        response = cleaned_data.get('response')
        if appointment_id and response:
            appointment = Appointment.objects.filter(pk=appointment_id).first()
            if not appointment:
                raise forms.ValidationError("Invalid appointment ID")
            if response not in ['accept', 'cancel', 'proposed']:
                raise forms.ValidationError("Invalid response")
            cleaned_data['appointment'] = appointment
        else:
            raise forms.ValidationError("Appointment ID and response are required")
        return cleaned_data




class RepportForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    remarques = forms.CharField(widget=forms.Textarea)
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), widget=forms.Select(attrs={'size': 1, 'id': 'doctor'}), required=False)
    medical_record = forms.ModelChoiceField(queryset=MedicalRecord.objects.all(), widget=forms.Select(attrs={'size': 1, 'id': 'medical_record'}),required=False)
    
    medical_history=forms.CharField(required=False)
    ongoing_treatment=forms.CharField(required=False)
    medications=forms.CharField(required=False)
    notes=forms.CharField(required=False)
    class Meta:
        model = Repport
        fields = ['disease', 'date', 'remarques', 'medical_history', 'ongoing_treatment','medications','notes', 'doctor', 'medical_record']
        
    def save(self, commit=True):
        repport = super().save(commit=False)
        if commit:
            repport.save()
        
        return repport
        

# class PrescriptionForm(forms.ModelForm):
#     class Meta:
#         model = Prescription
#         fields = ['date', 'city', 'notes']

# class MedicationForm(forms.ModelForm):
#     class Meta:
#         model = Medication
#         fields = ['name', 'notes']

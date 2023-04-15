from django.db import models
from accounts.models import Patient,Doctor,Receptionist
from django.utils import timezone

# Create your modelsx here.


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('proposed', 'Proposed'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(default=timezone.now)
    complete = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='requested')
    cause = models.CharField(max_length=100, blank=True, null=True) # field for cancellation reason

    def __str__(self):
        return f'{self.patient} - {self.doctor} - {self.date} - {self.time}'

    class Meta:
        ordering = ['date', 'time']

class MedicalRecord(models.Model):
    patient = models.OneToOneField(Patient,on_delete=models.CASCADE)
    def __str__(self):
        return self.patient.firstName
    
    

class Repport(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    disease = models.CharField(max_length=100)
    date = models.DateField()
    diagnostics = models.CharField(max_length=500, default='')
    medical_history = models.CharField(max_length=500, default='')
    ongoing_treatment = models.CharField(max_length=500, default='')
    remarques = models.CharField(max_length=500)
    medications = models.CharField(max_length=100)
    notes = models.CharField(max_length=500)

    def __str__(self):
        return self.medical_record.patient.firstName

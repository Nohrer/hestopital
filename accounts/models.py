from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_receptionist = models.BooleanField(default=False)
    

class Patient(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    birthDate = models.DateField(null=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    cin = models.CharField(max_length=8,default='')
    phoneNumber = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.firstName +" "+ self.lastName


class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    birthDate = models.DateField(null=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    cin = models.CharField(max_length=8,default='')
    phoneNumber = models.CharField(max_length=10)
    
    def __str__(self) :
        return self.lastName +" "+self.firstName+" ("+self.speciality+")"

    
    
class Receptionist(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    birthDate = models.DateField(null=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    cin = models.CharField(max_length=8,default='')
    phoneNumber = models.CharField(max_length=10)

    def __str__(self) :
        return self.lastName +" "+self.firstName

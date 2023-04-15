from django.contrib import admin
from .models import Appointment,MedicalRecord,Repport
from accounts.models import Doctor,Patient,Receptionist,User
# Register your models here.


admin.site.register(Doctor)
admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(MedicalRecord)
admin.site.register(Repport)
admin.site.register(Receptionist)


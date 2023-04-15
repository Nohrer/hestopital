# Generated by Django 4.1.6 on 2023-04-07 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_doctor_id_patient_id_receptionist_id_and_more'),
        ('main', '0003_rename_repportremarque_repport_remarques'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalrecord',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.patient'),
        ),
        migrations.AlterField(
            model_name='ordonnance',
            name='repport',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.repport'),
        ),
    ]
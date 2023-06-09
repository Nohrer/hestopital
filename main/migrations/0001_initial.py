# Generated by Django 4.1.6 on 2023-03-27 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Repport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('repportRemarque', models.CharField(max_length=500)),
                ('MedicalRecord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.medicalrecord')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Ordonnance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medications', models.CharField(max_length=100)),
                ('notes', models.CharField(max_length=500)),
                ('repport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.repport')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('hour', models.TimeField(default='hh:mm:ss')),
                ('complete', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('requested', 'Requested'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='requested', max_length=10)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_available', models.BooleanField(default=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.patient')),
            ],
        ),
    ]

# Generated by Django 4.1.6 on 2023-04-09 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_prescription_report_delete_medication_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordonnance',
            name='repport',
        ),
        migrations.AddField(
            model_name='repport',
            name='ordonnance',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.ordonnance'),
        ),
    ]
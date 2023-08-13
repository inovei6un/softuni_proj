# Generated by Django 4.1.4 on 2023-08-06 17:03

from django.db import migrations, models
import lawyer_site.models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyer_site', '0004_remove_appointment_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('document_file', models.FileField(upload_to=lawyer_site.models.document_upload_path)),
                ('category', models.CharField(choices=[('Гражданско право', 'Гражданско право'), ('Семейно право', 'Семейно право'), ('Административно право', 'Административно право'), ('Наказателно право', 'Наказателно право'), ('Търговско право', 'Търговско право'), ('Трудово право', 'Трудово право')], max_length=100)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
from django.core.exceptions import ValidationError
from django.db import models


class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f'{self.date} - {self.time}'

    class Meta:
        unique_together = ('date', 'time')


def document_upload_path(instance, filename):
    # Construct the upload path based on the category and filename
    return f"documents/{instance.category}/{filename}"


class Document(models.Model):
    CATEGORY_CHOICES = (
        ('Гражданско право', 'Гражданско право'),
        ('Семейно право', 'Семейно право'),
        ('Административно право', 'Административно право'),
        ('Наказателно право', 'Наказателно право'),
        ('Търговско право', 'Търговско право'),
        ('Трудово право', 'Трудово право'),
    )

    title = models.CharField(max_length=100)
    document_file = models.FileField(upload_to=document_upload_path)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

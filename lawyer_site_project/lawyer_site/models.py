from django.core.exceptions import ValidationError
from django.db import models
from lawyer_site.validators import validate_letters_only


class User(models.Model):
    first_name = models.CharField(
        max_length=20,
        validators=[validate_letters_only],
    )

    last_name = models.CharField(
        max_length=20,
        validators=[validate_letters_only],
    )

    email = models.EmailField(max_length=40, unique=True)

    password = models.CharField(
        max_length=30,
    )
    is_anonymous = False
    is_authenticated = True

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f'{self.date} - {self.time}'

    class Meta:
        unique_together = ('date', 'time')
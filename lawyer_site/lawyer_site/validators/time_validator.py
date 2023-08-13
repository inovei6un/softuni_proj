from django.core.exceptions import ValidationError
import datetime


def validate_time_not_after_4pm(value):
    try:
        # appointment_time = datetime.datetime.strptime(value, '%H:%M').time()
        closing_time = datetime.time(hour=16, minute=0)
        opening_time = datetime.time(hour=10, minute=0)
        if value > closing_time or value < opening_time:
            raise ValidationError('Часът трябва да бъде след 10:00 и преди 16:00!')
    except ValueError:
        raise ValidationError('Невалиден формат за час. Използвайте ЧЧ:ММ.')

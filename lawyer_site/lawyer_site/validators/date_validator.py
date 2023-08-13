from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_date_before_today(value):
    today = timezone.now().date()
    # date_value = datetime.strptime(value, '%Y-%m-%d').date()
    if value < today:
        raise ValidationError("Датата не може да бъде в миналото!")
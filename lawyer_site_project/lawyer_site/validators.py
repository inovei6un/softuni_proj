from django.core.exceptions import ValidationError


def validate_letters_only(value):
    if not value.isalpha():
        raise ValidationError('Името може да се състои само от букви!')

from django.core.exceptions import ValidationError


def price_validator(value):
    if value < 0:
        raise ValidationError("Price must be postive value")

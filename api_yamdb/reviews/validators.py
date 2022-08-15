from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value < 1700 or value > (timezone.now().year + 1):
        raise ValidationError('Неверный год. '
                              'Будущие реализы можно добавлять только если '
                              'выход не позднее следующего года')

from django.core.exceptions import ValidationError
from .models import MyUser
from django.contrib import messages

def validate_email(value):
    if MyUser.objects.filter(email = value).exists():
        raise ValidationError(
            ('Account with this email already exists'),
            params={'value':value}
        )
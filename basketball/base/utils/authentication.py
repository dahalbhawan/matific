from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError

def get_and_authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        raise ValidationError("Invalid username/password. Please try again!")
    return user
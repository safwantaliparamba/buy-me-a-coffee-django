import uuid
import random
import json
import requests
import string
from random import randint

from django.http.request import HttpRequest

from accounts.models import User


def randomnumber(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


"""
To get unique id's according to the length of n
"""


def generate_unique_id(n):
    unique_id = []

    characters = list(string.ascii_letters + string.digits)
    random.shuffle(characters)

    for i in range(n):
        unique_id.append(random.choice(characters))
    random.shuffle(unique_id)

    return "".join(unique_id)


"""
To get random password according to the length of n
"""


def random_password(n):
    password = []

    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    random.shuffle(characters)

    for i in range(n):
        password.append(random.choice(characters))
    random.shuffle(password)

    return "".join(password)


# function to join multiple serializer errors
def join_errors(_errors=[]):
    errors = {}
    for _error in _errors:
        if hasattr(_error, '_errors'):
            errors.update(_error._errors)

    return errors


def get_auto_id(model):
    auto_id = 1
    latest_auto_id = model.objects.all().order_by("-date_added")[:1]
    if latest_auto_id:
        for auto in latest_auto_id:
            auto_id = auto.auto_id + 1
    return auto_id


def is_valid_uuid(value):
    """
        to find the string is valid uuid 
    """
    try:
        uuid.UUID(str(value))

        return True
    except ValueError:
        return False


def get_client_ip(request: HttpRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def authenticate(request: HttpRequest, email: str, password: str):
    user: User = User.objects.filter(email=email).latest("date_joined")

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "email": email,
        "password": password,
    }

    print(data)

    protocol = "http://"

    if request.is_secure():
        protocol = "https://"

    host = request.get_host()
    url = protocol + host + "/api/v1/accounts/token/"

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response.json())

    if response.status_code == 200:

        return {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "email": user.email,
                "name": user.name,
                "refresh": response.json().get("refresh"),
                "access": response.json().get("access"),
            }
        }
    
    return {
        "statusCode": 6001,
        "data": {
            "title": "Failed",
            "message": "Token generation failed"
        }
    }

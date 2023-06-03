import uuid
import random
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


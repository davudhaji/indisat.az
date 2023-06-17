import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    regex = r'^\+?[0-9]{9,15}$'
    message = _(
        'Phone number is invalid. This may contain only digits. Allowed length is 9 - 15'
    )
    flags = 0


def my_check_phone_number(phone_number):
    pattern = r'^\+?[0-9]{9,15}$'
    if re.match(pattern, phone_number):
        return True
    return False


def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.match(regex, email)):
        return True
    return False


def my_check_password(password):
    regex = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&+=]).*$"
    if (re.match(regex, password)):
        return True
    return False

def check_only_letter_number(val):
    regex = '^[A-Za-z0-9]+$'
    if (re.match(regex, val)):
        return True
    return False

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()

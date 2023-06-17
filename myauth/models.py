from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

USER_MODEL = settings.AUTH_USER_MODEL


@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    regex = r"^\+?[0-9]{9,15}$"
    message = _(
        "Phone number is invalid. This may contain only digits. Allowed length is 9 - 15"
    )
    flags = 0


class MyUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _("email address"),
        max_length=255,
        unique=True,
        error_messages={
            "unique": _(
                "This email has already been registered. Please choose another one."
            ),
        },
    )

    phone_number = models.CharField(
        _("phone number"),
        max_length=15,
        null=True,
        validators=[PhoneNumberValidator()],
        error_messages={
            "unique": _(
                "This phone number has already registered. Choose another one, please"
            )
        },
    )
    first_name = models.CharField(_("first name"), max_length=60)
    last_name = models.CharField(_("last name"), max_length=60)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into the admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        return self.email

    def get_full_name(self):
        """
        Returns the first name and last name concatenated with a space.
        """
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name.strip()

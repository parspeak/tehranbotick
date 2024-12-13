from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.managers import UserManager
from django.utils import timezone


class User(AbstractBaseUser):
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    phone_number = models.CharField(
        _("Phone Number"),
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^09(0[0-5]|[1 3]\d|2[0-3]|9[0-9]|41)\d{7}$',
                message=_("Enter a valid phone number."),
                code="invalid_phone"
            )
        ]
    )
    is_active = models.BooleanField(_("Is Active"), default=False)
    is_admin = models.BooleanField(_("Is Admin"), default=False)

    otp = models.CharField(_("One-Time Password (OTP)"), max_length=5, null=True, blank=True)
    otp_expiry = models.DateTimeField(_("OTP Expiry"), blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def otp_is_expired(self):
        if self.otp_expiry and self.otp_expiry < timezone.now():
            return True
        return False

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def is_staff(self):
        return self.is_admin

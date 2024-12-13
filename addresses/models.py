from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name=_("User")
    )
    province = models.CharField(_("Province"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    postal_code = models.CharField(_("Postal Code"), max_length=10)
    address = models.TextField(_("Address"))
    full_name = models.CharField(_("Full Name"), max_length=50)
    phone_number = models.CharField(_("Phone Number"), max_length=11)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return self.full_name

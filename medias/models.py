from core.models import AbstractBaseModel
from accounts.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Image(AbstractBaseModel):
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="images",
        verbose_name=_("Created By")
    )
    last_modified_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Last Modified By")
    )
    name = models.CharField(_("Name"), max_length=255)
    alt_text = models.CharField(_("Alternative Text"), max_length=255)
    image = models.ImageField(
        _("Image"),
        upload_to='images/%Y/%m/%d/'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.name

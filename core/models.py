import uuid
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    last_modified = models.DateTimeField(_("Last Modified"), auto_now=True)

    class Meta:
        abstract = True


class AbstractNameDescriptionModel(models.Model):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    description = CKEditor5Field(_("Description"), blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AbstractSEOModel(models.Model):
    meta_title = models.CharField(
        _("Meta Title"),
        max_length=800,
        blank=True,
        null=True,
        help_text=_("Title for search engine optimization.")
    )
    meta_description = models.CharField(
        _("Meta Description"),
        max_length=350,
        blank=True,
        null=True,
        help_text=_("Description for search engines.")
    )
    slug = models.SlugField(_("Slug"), unique=True, allow_unicode=True)

    class Meta:
        abstract = True
        verbose_name = _("SEO Information")
        verbose_name_plural = _("SEO Information")


class AbstractPublishableModel(models.Model):
    published_date = models.DateField(_("Published Date"), blank=True, null=True, auto_now=True)
    published = models.BooleanField(_("Published"), default=False)

    class Meta:
        abstract = True


class AbstractUUIDModel(models.Model):
    alias = models.UUIDField(_("Alias"), default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class AbstractBaseUUIDModel(AbstractUUIDModel):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    last_modified = models.DateTimeField(_("Last Modified"), auto_now=True)

    class Meta:
        abstract = True

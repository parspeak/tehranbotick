from django.db import models
from datetime import datetime
from medias.models import Image
from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from products import ProductType, StockStatus, DiscountType, VariableType
from core.models import AbstractNameDescriptionModel, AbstractSEOModel, AbstractBaseModel, AbstractPublishableModel
from statistics import mean
from django.utils.translation import gettext_lazy as _


class Category(AbstractNameDescriptionModel, AbstractSEOModel):
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name=_("Parent Category")
    )
    thumbnail = models.ForeignKey(
        Image,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Thumbnail")
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Product(AbstractNameDescriptionModel, AbstractBaseModel, AbstractSEOModel, AbstractPublishableModel):
    summary = models.TextField(null=True, blank=True, verbose_name=_("Summary"))
    thumbnail = models.ForeignKey(
        Image,
        on_delete=models.PROTECT,
        verbose_name=_("Thumbnail")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Category")
    )
    type = models.CharField(
        max_length=25,
        default=ProductType.SIMPLE_PRODUCT,
        choices=ProductType.choices,
        verbose_name=_("Product Type")
    )
    related_to = models.ManyToManyField(
        "self",
        blank=True,
        verbose_name=_("Related Products")
    )
    discount_type = models.CharField(
        max_length=25,
        choices=DiscountType.choices,
        blank=True,
        null=True,
        verbose_name=_("Discount Type")
    )
    discount_value = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Discount Value"))
    discount_start_date = models.DateField(null=True, blank=True, verbose_name=_("Discount Start Date"))
    discount_end_date = models.DateField(null=True, blank=True, verbose_name=_("Discount End Date"))

    class Meta:
        ordering = ('name',)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def is_discounted(self):
        if self.discount_value and self.discount_start_date <= datetime.now().date() <= self.discount_end_date and self.discount_type:
            return True
        return False

    def get_price_text(self):
        return f'{format(min([product.price for product in self.variants.all()]), ",")} تومان'

    def get_discounted_price(self):
        if not self.is_discounted():
            return self.get_price_text()
        original_price = min([product.price for product in self.variants.all()])
        discounted_price = 0

        if self.discount_type == DiscountType.PERCENTAGE:
            # Calculate percentage discount
            discount_amount = (original_price * self.discount_value) / 100
            discounted_price = original_price - discount_amount
        elif self.discount_type == DiscountType.CONSTANT:
            discounted_price = original_price - self.discount_value

        return f'{format(max(int(discounted_price), 0), ",")} تومان'

    def in_stock(self):
        return mean([product.stock for product in self.variants.all()]) > 0

    def clean(self):
        if self.discount_type:
            if not self.discount_value:
                raise ValidationError(_("Discount value is required."))
            if not self.discount_start_date or not self.discount_end_date:
                raise ValidationError(_("Discount start and end dates are required."))

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        verbose_name=_("Product")
    )
    variant_image = models.ForeignKey(
        Image,
        on_delete=models.PROTECT,
        verbose_name=_("Variant Image")
    )
    price = models.PositiveIntegerField(verbose_name=_("Price"))
    track_inventory = models.BooleanField(default=True, verbose_name=_("Track Inventory"))
    variables = models.ManyToManyField("Variable", blank=True, verbose_name=_("Variables"))

    stock = models.PositiveSmallIntegerField(default=0, verbose_name=_("Stock"))

    stock_status = models.CharField(
        default=StockStatus.IN_STOCK,
        choices=StockStatus.choices,
        max_length=15,
        verbose_name=_("Stock Status")
    )

    def decrease_stock(self, quantity):
        if self.stock < quantity:
            raise ValueError(_("Not enough stock available."))
        self.stock -= quantity
        self.save()

    def increase_stock(self, quantity):
        self.stock += quantity
        self.save()

    class Meta:
        ordering = ('price',)
        verbose_name = _('Product Variant')
        verbose_name_plural = _('Product Variants')

    def get_price_text(self):
        return f'{format(self.price, ",")} تومان'

    def __str__(self):
        return f"{self.product.name} | {', '.join(x.name for x in self.variables.all())}"


class Variable(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    color = ColorField(null=True, blank=True, verbose_name=_("Color"))
    variant_thumbnail = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Variant Thumbnail")
    )
    type = models.CharField(
        max_length=20,
        choices=VariableType.choices,
        default=VariableType.COLOR,
        verbose_name=_("Variable Type")
    )

    class Meta:
        verbose_name = _('Variable')
        verbose_name_plural = _('Variables')

    def __str__(self):
        return self.name

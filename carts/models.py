from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from carts.managers import CartItemManager
from core.models import AbstractBaseModel
from products import DiscountType
from products.models import ProductVariant
from django.utils import timezone


class PromoCode(AbstractBaseModel):
    code = models.CharField(_("Promo Code"), max_length=255)
    code_type = models.CharField(
        _("Code Type"),
        max_length=25,
        choices=DiscountType.choices
    )
    value = models.IntegerField(_("Value"))
    expiration_date = models.DateTimeField(_("Expiration Date"))
    active = models.BooleanField(_("Active"), default=False)

    class Meta:
        verbose_name = _("Promo Code")
        verbose_name_plural = _("Promo Codes")

    def apply_discount(self, original_price):
        if self.code_type == DiscountType.CONSTANT:
            return max(0, original_price - self.value)
        elif self.code_type == DiscountType.PERCENTAGE:
            return max(0, original_price * (1 - (self.value / 100)))
        return original_price

    def is_valid(self):
        if self.active and self.expiration_date >= timezone.now():
            return True
        return False

    def __str__(self):
        return self.code


class CartItem(AbstractBaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cartitems",
        verbose_name=_("User")
    )
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        verbose_name=_("Product Variant")
    )
    quantity = models.PositiveIntegerField(_("Quantity"))
    deleted_or_paid = models.BooleanField(_("Deleted or paid"), default=False)

    objects = CartItemManager()

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")

    def get_price(self):
        return self.quantity * self.product_variant.price

    def get_discount(self):
        discount = 0
        if self.product_variant.product.is_discounted():
            if self.product_variant.product.discount_type == DiscountType.CONSTANT:
                discount = self.product_variant.product.discount_value
            elif self.product_variant.product.discount_type == DiscountType.PERCENTAGE:
                discount = (self.product_variant.price * self.product_variant.product.discount_value) / 100
        return discount

    def __str__(self):
        return self.user.phone_number

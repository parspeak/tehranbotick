from django.db import models
from accounts.models import User
from addresses.models import Address
from carts.models import CartItem, PromoCode
from core.models import AbstractBaseUUIDModel
from orders import OrderStatus
from django.utils.translation import gettext_lazy as _


class Order(AbstractBaseUUIDModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_("User")
    )
    cart_items = models.ManyToManyField(
        CartItem,
        related_name='orders',
        verbose_name=_("Cart Items")
    )
    status = models.CharField(
        max_length=25,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name=_("Status")
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0.0,
        verbose_name=_("Total Price")
    )
    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Promo Code")
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Address")
    )
    store_delivery = models.BooleanField(
        default=False,
        verbose_name=_("Store Delivery")
    )
    transaction_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Transaction ID")
    )

    def calculate_total(self):
        total = sum(item.get_price() - item.get_discount() for item in self.cart_items.all())

        if self.promo_code and self.promo_code.is_valid():
            total = self.promo_code.apply_discount(total)

        self.total_price = total
        return total

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def is_paid(self):
        return self.status == OrderStatus.PAID

    def __str__(self):
        return self.alias.hex

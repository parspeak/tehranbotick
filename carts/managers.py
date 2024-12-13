from django.db.models import Manager
from django.core.exceptions import ObjectDoesNotExist


class CartItemManager(Manager):
    def update_or_create(self, **kwargs):
        quantity = kwargs.pop('quantity', None)
        try:
            instance = self.get(**kwargs, deleted_or_paid=False)
            instance.quantity = quantity
            instance.save()
            return instance, None
        except ObjectDoesNotExist:
            instance = self.create(**kwargs, quantity=quantity)
            return None, instance

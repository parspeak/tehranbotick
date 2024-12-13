from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_telegram_message_task
from . import OrderStatus
from .models import Order


@receiver(post_save, sender=Order)
def order_paid(sender, instance, created, **kwargs):
    if not created and instance.status == OrderStatus.PAID:
        send_telegram_message_task.delay(instance.id)

from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', 'در انتظار پرداخت'
    PAID = 'PAID', 'پرداخت شده'
    # SHIPPED = 'SHIPPED', 'ارسال شده'
    COMPLETED = 'COMPLETED', 'تکمیل شده'
    CANCELED = 'CANCELED', 'لغو شده'

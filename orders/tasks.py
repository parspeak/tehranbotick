from celery import shared_task
from orders.models import Order, OrderStatus
import requests
from django.conf import settings

TELEGRAM_TOKEN = settings.TELEGRAM_BOT_TOKEN
CHAT_ID = settings.TELEGRAM_CHAT_ID

@shared_task
def restore_stock_on_payment_failure(order_id):
    """بازگرداندن موجودی در صورت عدم موفقیت پرداخت."""
    try:
        order = Order.objects.get(id=order_id)
        if order.status == OrderStatus.PENDING:
            for item in order.cart_items.all():
                item.product_variant.increase_stock(item.quantity)
            order.status = OrderStatus.CANCELED
            order.save()
    except Order.DoesNotExist:
        pass


@shared_task
def delete_product_from_cart(order_id):
    try:
        order = Order.objects.get(id=order_id)
        for item in order.cart_items.all():
            item.deleted_or_paid = True
            item.save()
    except Order.DoesNotExist:
        pass


@shared_task
def send_telegram_message_task(order_id):
    from .models import Order  # وارد کردن مدل برای استفاده در وظیفه
    try:
        order = Order.objects.get(id=order_id)
        message = ""

        if order.store_delivery:
            message = f"""
📦 سفارش جدید 🚚

🔹 نام و نام خانوادگی: {order.user.first_name} {order.user.last_name}
🔹 شماره تلفن: {order.user.phone_number}
🔹 محل تحویل: درب فروشگاه

🛒 جزئیات سفارش:
"""
        else:
            message = f"""
📦 سفارش جدید 🚚

🔹 استان: {order.address.province}
🔹 شهر: {order.address.city}
🔹 کد پستی: {order.address.postal_code}
🔹 آدرس: {order.address.address}
🔹 نام و نام خانوادگی: {order.address.full_name}
🔹 شماره تلفن: {order.address.phone_number}

🛒 جزئیات سفارش:
"""
        for cart_item in order.cart_items.all():
            message += f"🔹 تعداد: {cart_item.quantity} | محصول: {cart_item.product_variant}\n"

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown',
        }

        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"خطا در ارسال پیام تلگرام: {response.text}")

    except Order.DoesNotExist:
        print(f"Order با id={order_id} یافت نشد.")
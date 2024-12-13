from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from addresses.models import Address
from orders import OrderStatus
from orders.models import Order
from carts.forms import PromoCodeForm
from carts.models import PromoCode, CartItem
from core.views import ProtectedView
from django_htmx.http import HttpResponseClientRedirect
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException
from .tasks import restore_stock_on_payment_failure, delete_product_from_cart
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required


def create_transaction(request, phone_number, order):
    factory = bankfactories.BankFactory()
    try:
        bank = (
            factory.auto_create()
        )
        bank.set_request(request)
        bank.set_amount(order.total_price)
        bank.set_client_callback_url(callback_url=reverse('orders:callback-view'))
        bank.set_mobile_number(phone_number)
        bank_record = bank.ready()
        order.transaction_id = bank_record.id
        order.save()
        url = bank.get_gateway()['url']
        if request.htmx:
            return HttpResponseClientRedirect(url)
        return redirect(url)
    except AZBankGatewaysException as e:
        messages.error(request, e)
        return render(request, template_name="partials/alert.html")


class CreateOrderView(ProtectedView):
    def post(self, request):
        promo_code = None
        if request.POST.get('code'):
            form = PromoCodeForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data['code']
                try:
                    promo_code = PromoCode.objects.get(code__iexact=code, active=True)
                    if not promo_code.is_valid():
                        messages.error(request, "کد تخفیف منقضی شده است، لطفا از کد تخفیف دیگری استفاده کنید.")
                        return render(request, "partials/alert.html")
                except PromoCode.DoesNotExist:
                    messages.error(request, "کد تخفیف معتبر نیست.")
                    return render(request, "partials/alert.html")
            else:
                messages.error(request, "کد تخفیف نامعتبر است.")
                return render(request, "partials/alert.html")

        cart_items = CartItem.objects.filter(user=request.user, deleted_or_paid=False)
        if not cart_items.exists():
            messages.error(request, "سبد خرید شما خالی است.")
            return render(request, "partials/alert.html")

        order = Order.objects.create(user=request.user, promo_code=promo_code)
        order.cart_items.set(cart_items)
        order.save()
        order.total_price = order.calculate_total()
        order.save()

        if request.htmx:
            return HttpResponseClientRedirect(reverse('addresses:addresses-view'))
        return redirect('addresses:addresses-view')


class CheckoutView(ProtectedView):
    def redirect(self, request, to):
        if request.htmx:
            return HttpResponseClientRedirect(reverse(to))
        return redirect(to)

    def post(self, request):
        order = Order.objects.prefetch_related(
            "cart_items__product_variant", "cart_items__product_variant__product"
        ).filter(user=self.request.user)
        last_order = order.last()

        if not order.exists() or (last_order.status != OrderStatus.PENDING) or (last_order.transaction_id is not None):
            messages.error(request, "شما سفارش فعالی ندارید برای ادامه از دکمه 'ثبت سفارش' استفاده نمایید.")
            return self.redirect(request, 'carts:list-cart-view')

        addresses = Address.objects.filter(user=request.user, default=True)
        if not last_order.store_delivery:
            if not addresses.exists():
                messages.error(request, "لطفا یک آدرس را به عنوان پیشفرض قرار دهید و یا از گزینه تحویل درب فروشگاه استفاده نمایید.")
                return render(request, template_name="partials/alert.html")
            else:
                last_order.address = addresses.last()

        cart_items = last_order.cart_items.all()
        for item in cart_items:
            if item.quantity > item.product_variant.stock:
                messages.error(
                    request, f"{item.product_variant.product.name} با تعداد {item.quantity} در انبار موجود نیست."
                )
                return self.redirect(request, 'carts:list-cart-view')

        try:
            with transaction.atomic():
                for item in cart_items:
                    item.product_variant.decrease_stock(item.quantity)
                last_order.save()

                restore_stock_on_payment_failure.apply_async(
                    (last_order.id,),
                    countdown=20 * 60  # مدت زمان رزرو (30 دقیقه)
                )
        except Exception as e:
            messages.error(request, "خطایی در کاهش موجودی محصولات رخ داده است.")
            return self.redirect(request, 'carts:list-cart-view')

        return create_transaction(request, phone_number=request.user.phone_number, order=last_order)


def callback(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        return render(request, template_name="orders/checkout-failed.html", context={
            'message': 'این لینک معتبر نیست.'
        })

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        return render(request, template_name="orders/checkout-failed.html", context={
            'message': 'این لینک معتبر نیست.'
        })

    order = Order.objects.filter(transaction_id=bank_record.id).first()
    if bank_record.is_success:
        order.status = OrderStatus.PAID
        order.save()
        delete_product_from_cart.apply_async(args=(order.id,))
        return render(request, template_name="orders/checkout-successfully.html")

    return render(request, template_name="orders/checkout-failed.html", context={
        'message': 'پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.'
    })


@method_decorator(staff_member_required, name='dispatch')
class GenerateOrderPDF(View):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(status=OrderStatus.PAID) \
            .select_related('address') \
            .prefetch_related('cart_items__product_variant')

        grouped_orders = list(chunk_orders(list(orders), chunk_size=3))

        context = {'grouped_orders': grouped_orders}
        html_content = render_to_string('orders/orders-list.html', context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="orders.pdf"'
        HTML(string=html_content).write_pdf(response)
        return response


def chunk_orders(orders, chunk_size=3):
    for i in range(0, len(orders), chunk_size):
        yield orders[i:i + chunk_size]

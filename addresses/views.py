from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django_htmx.http import HttpResponseClientRedirect
from addresses.forms import AddressFrom
from addresses.models import Address
from carts.views import BaseCartView
from core.views import ProtectedView
from orders import OrderStatus
from orders.models import Order
from django.conf import settings


# Create your views here.
class AddressView(BaseCartView):
    template_name = "addresses/index.html"
    form_class = AddressFrom

    def dispatch(self, request, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user)
        if not order.exists() or order.last().status != OrderStatus.PENDING:
            messages.error(request, "شما سفارش فعالی ندارید برای ادامه از دکمه 'ثبت سفارش' استفاده نمایید.")
            return redirect('carts:list-cart-view')
        return super(AddressView, self).dispatch(request, *args, **kwargs)

    def get_context(self):
        promo_code_discount = 0
        context = super(AddressView, self).get_context()
        order = Order.objects.filter(user=self.request.user).last()

        if order.promo_code:
            promo_code_discount = context['purchase_price_int'] - int(
                order.promo_code.apply_discount(context['purchase_price_int']))

        if not order.store_delivery:
            context['shipping_cost'] = f'{format(settings.SHIPPING_COST, ",")} تومان'

        return {
            **context,
            'addresses': Address.objects.filter(user=self.request.user),
            'promo_code_discount': f'{format(promo_code_discount, ",") if order.promo_code else promo_code_discount} تومان',
            'purchase_price': f'{format(order.total_price, ",") if order.store_delivery else format(order.total_price + settings.SHIPPING_COST, ",")} تومان',
            'store_delivery': order.store_delivery,
            'form': self.form_class,
        }

    def get(self, request):
        return self.render_html()

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.save()
            return render(request, template_name=f"{self.template_name}#address", context={'address': instance})

        response = render(request, template_name=f"{self.template_name}#add-form", context={'form': form})
        response['HX-Reswap'] = 'outerHTML'
        response['HX-Retarget'] = '#add-form'
        return response


class DeliveryStoreView(ProtectedView):
    template_name = "addresses/index.html"

    def post(self, request):
        user = request.user
        order = Order.objects.filter(user=user).last()

        if not order:
            messages.error(request, "سفارشی برای شما یافت نشد.")
            if request.htmx:
                return HttpResponseClientRedirect(reverse('carts:list-cart-view'))
            return redirect('carts:list-cart-view')

        order.store_delivery = not order.store_delivery
        order.save()

        if order.store_delivery:
            purchase_price = order.total_price
            shipping_cost = 0
        else:
            purchase_price = order.total_price + settings.SHIPPING_COST
            shipping_cost = settings.SHIPPING_COST

        context = {
            'purchase_price': f"{format(int(purchase_price), ',')} تومان",
            'shipping_cost': f"{format(int(shipping_cost), ',')} تومان"
        }

        return render(request, self.template_name+"#shipping", context)


class AddressDeleteView(ProtectedView):
    template_name = "addresses/index.html"

    def delete(self, request, pk):
        order = Order.objects.filter(address_id=pk, user=request.user)
        if order.exists():
            messages.error(request, message="سفارش فعال با این آدرس موجود است، لطفا بعدا دوباره امتحان کنید.")
            response = render(request, template_name="partials/alert.html")
            response['HX-Reswap'] = 'innerHTML'
            response['HX-Retarget'] = f'#messages'
            return response

        instance = Address.objects.filter(pk=pk, user=request.user)
        if instance.exists():
            instance.delete()
            addresses = Address.objects.filter(user=request.user)
            return render(request, template_name=f"{self.template_name}#address-list", context={'addresses': addresses})
        messages.error(request, message="شما دسترسی به حذف آدرس مورد نظر ندارید.")
        response = render(request, template_name="partials/alert.html")
        response['HX-Reswap'] = 'innerHTML'
        response['HX-Retarget'] = f'#messages'
        return response


class AddressUpdateView(ProtectedView):
    template_name = "addresses/index.html"
    form_class = AddressFrom

    def post(self, request, pk):
        form = self.form_class(request.POST, instance=Address.objects.filter(pk=pk, user=request.user).first())
        if form.is_valid():
            form.save()
            addresses = Address.objects.filter(user=request.user)
            return render(
                request,
                template_name=f"{self.template_name}#address-list", context={'form': form, 'addresses': addresses}
            )

        address = Address.objects.filter(user=request.user, pk=pk).first()
        response = render(
            request,
            template_name=f"{self.template_name}#edit-form", context={'form': form, 'address': address}
        )
        response['HX-Reswap'] = 'outerHTML'
        response['HX-Retarget'] = f'#edit-form-{pk}'
        return response


class AddressDefaultView(ProtectedView):
    template_name = "addresses/index.html"
    form_class = AddressFrom

    def post(self, request, pk):
        addresses = Address.objects.filter(user=request.user, default=True)
        for address in addresses:
            address.default = False
            address.save()

        instance = get_object_or_404(Address, user=request.user, pk=pk)
        instance.default = True
        instance.save()

        return render(
            request,
            template_name=f"{self.template_name}#address-list",
            context={'form': self.form_class(), 'addresses': Address.objects.filter(user=request.user)}
        )

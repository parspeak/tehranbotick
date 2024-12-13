from django.contrib import messages
from django.http import QueryDict
from django.shortcuts import render, get_object_or_404
from carts.forms import PromoCodeForm
from carts.models import CartItem, PromoCode
from core.views import ProtectedView
from products.models import ProductVariant


# Create your views here.
class BaseCartView(ProtectedView):
    template_name = "carts/basket.html"

    def get_context(self):
        queryset = CartItem.objects.select_related(
            "product_variant",
            "product_variant__variant_image",
            "product_variant__product"
        ).filter(user=self.request.user, deleted_or_paid=False)

        total_price = sum([x.get_price() for x in queryset])
        total_discount = sum([x.get_discount() for x in queryset])

        return {
            'total_price': f"{format(total_price, ',')} تومان",
            'total_discount': f"{format(int(total_discount), ',')} تومان",
            'purchase_price': f"{format(int(total_price - total_discount), ',')} تومان",
            'purchase_price_int': int(total_price - total_discount),
            'promo_code_discount': '0 تومان',
            'shipping_cost': f"0 تومان",
            'promo_code_form': PromoCodeForm(),
            'cartitems': queryset
        }

    def render_html(self, section=""):
        context = self.get_context()
        return render(self.request, template_name=self.template_name + section, context=context)


class CartView(BaseCartView):
    variant = None
    body = None

    def setup(self, request, *args, **kwargs):
        if request.method != 'GET':
            self.variant = get_object_or_404(ProductVariant, pk=kwargs.get('pk'))
        self.body = QueryDict(request.body)

        super().setup(request, *args, **kwargs)

    def is_valid_stock(self, stock):
        if stock is None or not stock.isdigit():
            messages.warning(self.request, message='تعداد محصول انتخاب نشده است.')
            return False
        elif int(stock) > self.variant.stock:
            messages.warning(self.request,
                             message=f'"{self.variant.product.name + " - " + ", ".join([x.name for x in self.variant.variables.all()])}" با این تعداد در انبار موجود نیست.')
            return False
        return True

    def is_valid_variant(self):
        if self.variant is None:
            messages.error(self.request, message='این محصول موجود نیست.')
            return False
        return True

    def update_or_create(self, stock):
        return CartItem.objects.update_or_create(
            user=self.request.user,
            product_variant=self.variant,
            quantity=stock,
        )

    def post(self, request, pk):
        stock = self.body.get('stock')

        if not self.is_valid_stock(stock):
            return render(request, template_name="partials/alert.html")

        if not self.is_valid_variant():
            return render(request, template_name="partials/alert.html")

        self.update_or_create(stock)

        message = f'{self.variant.product.name} با موفقیت به سبد خرید اضافه شد.'
        messages.success(request, message=f'{self.variant.product.name} با موفقیت به سبد خرید اضافه شد.')
        return render(request, template_name="partials/alert.html", context={'type': 'success', 'message': message})

    def patch(self, request, pk):
        cart = CartItem.objects.get(user=request.user, product_variant=self.variant, deleted_or_paid=False)

        if self.body.get("type") == "increase":
            stock = cart.quantity + 1

            if not self.is_valid_stock(str(stock)):
                return self.render_html("#basket")

            if not self.is_valid_variant():
                return self.render_html("#basket")
        else:
            if cart.quantity == 1:
                cart.delete()
                return self.render_html("#basket")
            else:
                stock = cart.quantity - 1

        self.update_or_create(stock)

        return self.render_html("#basket")

    def delete(self, request, pk):
        cart = CartItem.objects.get(user=request.user, product_variant=self.variant)
        cart.deleted_or_paid = True
        cart.save()
        return self.render_html("#basket")

    def get(self, request):
        return self.render_html()


class PromoCodeView(BaseCartView):
    promo_code = None

    def get_context(self):
        context = super(PromoCodeView, self).get_context()

        if self.promo_code:
            purchase_price = context.get('purchase_price_int', 0)

            discount_price = self.promo_code.apply_discount(purchase_price)
            discount_amount = purchase_price - discount_price

            context['promo_code_discount'] = f"{format(int(discount_amount), ',')} تومان"
            context['purchase_price'] = f"{format(int(discount_price), ',')} تومان"
            context['promo_code_form'] = PromoCodeForm(initial={'code': self.promo_code.code})
        return context

    def post(self, request):
        form = PromoCodeForm(request.POST)

        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                self.promo_code = PromoCode.objects.get(code__iexact=code, active=True)

                if not self.promo_code.is_valid():
                    messages.error(request, 'کد تخفیف شما منقضی شده است.')
                    return self.render_html("#basket")

                messages.success(request, 'کد تخفیف با موفقیت ثبت شد.')
                return self.render_html("#basket")

            except PromoCode.DoesNotExist:
                messages.error(request, 'کد تخفیف شما معتبر نمی‌باشد.')
                return self.render_html("#basket")

        messages.error(request, 'کد تخفیف شما معتبر نمی‌باشد.')
        return self.render_html("#basket")

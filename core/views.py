from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django_htmx.http import HttpResponseClientRedirect
from products import DiscountType
from products.models import Product
from datetime import datetime


class HomeView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = {
            'products': Product.objects.all().order_by('-id')[0:8],
            'discounted_products': Product.objects.filter(discount_start_date__lte=datetime.now().date(), discount_end_date__gte=datetime.now().date(), discount_type__in=[DiscountType.CONSTANT, DiscountType.PERCENTAGE]).distinct()[0:10],
            'categories_0': Product.objects.filter(category_id=2)[0:10],
            'categories_1': Product.objects.filter(category_id=3)[0:10],

        }
        return render(request, template_name=self.template_name, context=context)


class ProtectedView(View):
    def has_permissions(self):
        return not self.request.user.is_authenticated

    def dispatch(self, request, *args, **kwargs):
        if self.has_permissions():
            messages.warning(request, message='برای استفاده از سبد خرید باید وارد حساب کاربری خود شوید.')
            if request.htmx:
                return HttpResponseClientRedirect(reverse('accounts:user-login-view'))
            return redirect(reverse('accounts:user-login-view'))
        return super().dispatch(request, *args, **kwargs)

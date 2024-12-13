from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django_htmx.http import HttpResponseClientRedirect
from django.views.generic import View
from accounts.forms import LoginForm, VerifyOtpFrom, SignupForm, UserProfileUpdateForm
from accounts.models import User
from random import randint
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from accounts.tasks import send_otp
from orders import OrderStatus
from orders.models import Order
from django.urls import reverse


class LoginView(View):
    template_name = "accounts/login.html"
    confirm_template_name = "accounts/login-otp-form.html"

    form_class = LoginForm
    confirm_form_class = VerifyOtpFrom

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.htmx:
                return HttpResponseClientRedirect(reverse('home'))
            return redirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'form': self.form_class()
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            users = User.objects.filter(phone_number=form.cleaned_data.get("phone_number"))
            if users.exists():
                otp = randint(10000, 99999)
                user = users.first()
                user.otp = otp
                user.otp_expiry = timezone.now() + timedelta(seconds=settings.EXPIRE_OTP)
                user.save()
                send_otp.apply_async((form.cleaned_data.get("phone_number"), otp), )
            context = {
                'form': self.confirm_form_class(initial={'phone_number': form.cleaned_data.get("phone_number")}),
            }
            return render(request, template_name=self.confirm_template_name, context=context)
        return render(request, template_name=f"{self.template_name}#login_form", context={'form': form})


class VerifyLogin(View):
    form_class = VerifyOtpFrom
    template_name = "accounts/login-otp-form.html"
    success_url = reverse_lazy('home')

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(phone_number=cd.get('phone_number'))
            login(request=request, user=user)
            user.otp = None
            user.otp_expiry = None
            user.save()
            return HttpResponseClientRedirect(redirect_to=self.success_url)
        return render(request, template_name=f"{self.template_name}#verify_otp_form", context={'form': form})


class SignupView(View):
    template_name = "accounts/signup.html"
    confirm_template_name = "accounts/signup-otp-form.html"
    form_class = SignupForm
    confirm_form_class = VerifyOtpFrom

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.htmx:
                return HttpResponseClientRedirect(reverse('home'))
            return redirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'form': self.form_class()
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.filter(phone_number=cd.get("phone_number")).first()
            otp = randint(10000, 99999)
            if user:
                user.first_name = cd.get("first_name")
                user.last_name = cd.get("last_name")
                user.set_password(cd.get("password"))
                user.otp = otp
                user.otp_expiry = timezone.now() + timedelta(seconds=settings.EXPIRE_OTP)
                user.save()
            else:
                instance = User()
                instance.first_name = cd.get("first_name")
                instance.last_name = cd.get("last_name")
                instance.phone_number = cd.get("phone_number")
                instance.otp = otp
                instance.set_password(cd.get("password"))
                instance.otp_expiry = timezone.now() + timedelta(seconds=settings.EXPIRE_OTP)
                instance.save()
            send_otp.apply_async((cd.get("phone_number"), otp), )
            context = {
                'form': self.confirm_form_class(initial={'phone_number': cd.get("phone_number")})
            }
            return render(request, template_name=self.confirm_template_name, context=context)
        return render(request, template_name=f"{self.template_name}#signup_form", context={'form': form})


class VerifySignup(View):
    form_class = VerifyOtpFrom
    template_name = "accounts/signup-otp-form.html"
    success_url = reverse_lazy('accounts:user-login-view')

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(phone_number=cd.get('phone_number'))
            user.is_active = True
            user.otp = None
            user.otp_expiry = None
            user.save()
            return HttpResponseClientRedirect(redirect_to=self.success_url)
        return render(request, template_name=f"{self.template_name}#verify_otp_form", context={'form': form})


class ProfileDetailView(LoginRequiredMixin, View):
    template_name = "accounts/profile-detail.html"
    form_class = UserProfileUpdateForm

    def get(self, request):
        context = {
            'form': self.form_class(initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            })
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "اطلاعات پروفایل کاربری با موفقیت بروزرسانی شد.")
            return render(request, template_name="partials/alert.html")
        messages.error(request, form.errors)
        return render(request, template_name="partials/alert.html")


class ProfileOrdersView(LoginRequiredMixin, View):
    template_name = "accounts/profile-orders.html"

    def get(self, request):
        user_orders = Order.objects.prefetch_related("cart_items__product_variant__variant_image").filter(user=request.user)
        context = {
            'complete_orders': user_orders.filter(status__in=[OrderStatus.COMPLETED, OrderStatus.PAID]),
            'canceled_orders': user_orders.filter(status=OrderStatus.CANCELED)
        }
        return render(request, self.template_name, context)


def logout_view(request):
    logout(request)
    return redirect('home')

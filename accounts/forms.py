from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from accounts.models import User
import re


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput)
    confirm_password = forms.CharField(label=_('confirm password'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['phone_number', 'first_name', 'last_name']

    def clean_confirm_password(self):
        # Check that the two password entries match
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError(_("Passwords don't match"))
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['confirm_password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['phone_number', 'first_name', 'last_name', 'is_active', 'is_admin']


class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11, min_length=11)

    def clean_phone_number(self):
        cd = super().clean()
        phone_number = cd.get('phone_number')

        if not re.match(
                '^09((14)|(13)|(12)|(19)|(18)|(17)|(15)|(16)|(11)|(10)|(90)|(91)|(92)|(93)|(94)|(95)|(96)|(32)|(30)|(33)|(35)|(36)|(37)|(38)|(39)|(00)|(01)|(02)|(03)|(04)|(05)|(41)|(20)|(21)|(22)|(23)|(31)|(34)|(9910)|(9911)|(9913)|(9914)|(9999)|(999)|(990)|(9810)|(9811)|(9812)|(9813)|(9814)|(9815)|(9816)|(9817)|(998))\d{7}$', phone_number):
            raise ValidationError('شماره تلفن همراه نا معتبر است.')
        return phone_number


class VerifyOtpFrom(forms.Form):
    phone_number = forms.CharField(max_length=11, min_length=11)
    otp = forms.CharField(max_length=5, min_length=5)

    def clean_otp(self):
        cd = super().clean()
        users = User.objects.filter(phone_number=cd.get('phone_number'), otp=cd.get('otp'))
        if not users.exists() or users.first().otp_is_expired():
            raise ValidationError('کد تایید صحیح نمی باشد لطفا دوباره تلاش کنید.')


class SignupForm(forms.Form):
    first_name = forms.CharField(min_length=2, max_length=50)
    last_name = forms.CharField(min_length=2, max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=16)
    phone_number = forms.CharField(max_length=11, min_length=11)

    def clean_phone_number(self):
        cd = super().clean()
        phone_number = cd.get('phone_number')

        if not re.match(
                '^09((14)|(13)|(12)|(19)|(18)|(17)|(15)|(16)|(11)|(10)|(90)|(91)|(92)|(93)|(94)|(95)|(96)|(32)|(30)|(33)|(35)|(36)|(37)|(38)|(39)|(00)|(01)|(02)|(03)|(04)|(05)|(41)|(20)|(21)|(22)|(23)|(31)|(34)|(9910)|(9911)|(9913)|(9914)|(9999)|(999)|(990)|(9810)|(9811)|(9812)|(9813)|(9814)|(9815)|(9816)|(9817)|(998))\d{7}$',
                phone_number):
            raise ValidationError('شماره تلفن همراه نا معتبر است.')

        user = User.objects.filter(phone_number=phone_number, is_active=True).first()
        if user:
            raise ValidationError('کاربری با این مشخصات قبلا ثبت نام کرده است.')

        return phone_number


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

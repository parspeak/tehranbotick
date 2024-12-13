from django import forms
from carts.models import PromoCode
from django.core.exceptions import ValidationError


class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = ('code',)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        queryset = PromoCode.objects.filter(code__exact=code)
        if queryset.exists():
            instance = queryset.first()
            if instance.is_valid():
                return code
            raise ValidationError('کد تخفیف شما معتبر نمی باشد.')
        raise ValidationError('کد تخفیف شما معتبر نمی باشد.')

from django import forms
from addresses.models import Address


class AddressFrom(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('province', 'city', 'postal_code', 'address', 'full_name', 'phone_number')
        widgets = {
            'address': forms.TextInput()
        }

from django.contrib import admin
from carts.models import PromoCode


# Register your models here.
@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'code_type', 'value', 'expiration_date', 'active']

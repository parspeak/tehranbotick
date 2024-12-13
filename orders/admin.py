from django.contrib import admin
from orders import OrderStatus
from orders.models import Order


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'alias',
        'status',
        'total_price',
        'store_delivery',
    )
    list_filter = ('status', 'store_delivery')
    search_fields = ('user__username', 'transaction_id')
    actions = ['mark_as_paid', 'mark_as_canceled', 'mark_as_completed']

    @admin.action(description='علامت‌گذاری به‌عنوان پرداخت شده')
    def mark_as_paid(self, request, queryset):
        updated_count = queryset.update(status=OrderStatus.PAID)
        self.message_user(request, f'{updated_count} سفارش با موفقیت به وضعیت پرداخت شده تغییر یافت.')

    @admin.action(description='علامت‌گذاری به‌عنوان لغو شده')
    def mark_as_canceled(self, request, queryset):
        updated_count = queryset.update(status=OrderStatus.CANCELED)
        self.message_user(request, f'{updated_count} سفارش با موفقیت به وضعیت لغو شده تغییر یافت.')

    @admin.action(description='علامت‌گذاری به‌عنوان تکمیل شده')
    def mark_as_completed(self, request, queryset):
        updated_count = queryset.update(status=OrderStatus.COMPLETED)
        self.message_user(request, f'{updated_count} سفارش با موفقیت به وضعیت تکمیل شده تغییر یافت.')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        extra_context = extra_context or {}
        extra_context['order'] = obj

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    change_form_template = 'orders/admin/change_form.html'
    change_list_template = 'orders/admin/change_list.html'

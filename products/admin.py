from django.contrib import admin
from products.models import Category, Product, ProductVariant, Variable


# Register your models here.
class CategoryInline(admin.StackedInline):
    model = Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    raw_id_fields = ("thumbnail",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = (CategoryInline,)

    def get_queryset(self, request):
        return self.model.objects.filter(parent=None)


@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    autocomplete_fields = ("variant_thumbnail", )


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    autocomplete_fields = ("variables", )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Product Details", {"fields": ("name", "description", "summary", "thumbnail", "related_to", "category", "type")}),
        ("Discount", {"fields": ("discount_type", "discount_value", ("discount_start_date", "discount_end_date"))}),
        ("SEO Information", {"fields": [("meta_title", "meta_description", "slug")]}),
        ("Published", {"fields": ["published_date", "published"]}),
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    readonly_fields = ("published_date",)
    autocomplete_fields = ("related_to", "thumbnail",)
    inlines = (ProductVariantInline,)
    list_display = ("name", "is_discounted")

from django.contrib import admin
from medias.models import Image
from django.utils.html import format_html


# Register your models here.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by', 'last_modified_by', 'image_preview')
    list_filter = ('created_by', 'last_modified_by')
    search_fields = ('name', 'alt_text')
    readonly_fields = ('last_modified_by',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.last_modified_by = request.user
        super().save_model(request, obj, form, change)

    def image_preview(self, obj):
        if obj.image:
            return format_html(f"<img width='100' src='{obj.image.url}' />")
        return "No Image"
    image_preview.short_description = "Preview"

from rest_framework import serializers

from medias.serializers import ImageSerializer
from products.models import Category, Product, ProductVariant


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    sub_categories = serializers.SerializerMethodField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'description',
            'meta_title',
            'meta_description',
            'thumbnail',
            'slug',
            'sub_categories',
            'parent'
        )
        extra_kwargs = {
            'parent': {
                'write_only': True
            }
        }

    def get_sub_categories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ('id', 'product', 'variant_image', 'price', 'track_inventory', 'variables', 'stock', 'stock_status')


class ProductSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    last_modified = serializers.DateTimeField(read_only=True)
    published_date = serializers.DateField(read_only=True)
    category_name = serializers.CharField(read_only=True, source='category')
    variants = ProductVariantSerializer(many=True, read_only=True)
    price_text = serializers.SerializerMethodField(read_only=True)
    thumbnail = ImageSerializer()

    class Meta:
        model = Product
        fields = (
            'id',
            'created_at',
            'last_modified',
            'published_date',
            'name',
            'description',
            'meta_title',
            'meta_description',
            'slug',
            'published',
            'summary',
            'type',
            'discount_type',
            'discount_value',
            'discount_start_date',
            'discount_end_date',
            'thumbnail',
            'price_text',
            'category',
            'category_name',
            'related_to',
            'variants'
        )

    def get_price_text(self, instance):
        return instance.get_price_text()
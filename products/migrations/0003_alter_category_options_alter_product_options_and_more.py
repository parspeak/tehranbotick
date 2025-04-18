# Generated by Django 5.1.3 on 2024-12-08 14:42

import colorfield.fields
import django.db.models.deletion
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0002_alter_image_options_alter_image_alt_text_and_more'),
        ('products', '0002_alter_category_description_alter_product_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',), 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='productvariant',
            options={'ordering': ('price',), 'verbose_name': 'Product Variant', 'verbose_name_plural': 'Product Variants'},
        ),
        migrations.AlterModelOptions(
            name='variable',
            options={'verbose_name': 'Variable', 'verbose_name_plural': 'Variables'},
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description',
            field=models.CharField(blank=True, help_text='Description for search engines.', max_length=350, null=True, verbose_name='Meta Description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_title',
            field=models.CharField(blank=True, help_text='Title for search engine optimization.', max_length=800, null=True, verbose_name='Meta Title'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='products.category', verbose_name='Parent Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(allow_unicode=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='category',
            name='thumbnail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='medias.image', verbose_name='Thumbnail'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Discount End Date'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Discount Start Date'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_type',
            field=models.CharField(blank=True, choices=[('PERCENTAGE', 'Percentage'), ('FIXED', 'Fixed')], max_length=25, null=True, verbose_name='Discount Type'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_value',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Discount Value'),
        ),
        migrations.AlterField(
            model_name='product',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Last Modified'),
        ),
        migrations.AlterField(
            model_name='product',
            name='meta_description',
            field=models.CharField(blank=True, help_text='Description for search engines.', max_length=350, null=True, verbose_name='Meta Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='meta_title',
            field=models.CharField(blank=True, help_text='Title for search engine optimization.', max_length=800, null=True, verbose_name='Meta Title'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Published'),
        ),
        migrations.AlterField(
            model_name='product',
            name='published_date',
            field=models.DateField(auto_now=True, null=True, verbose_name='Published Date'),
        ),
        migrations.AlterField(
            model_name='product',
            name='related_to',
            field=models.ManyToManyField(blank=True, to='products.product', verbose_name='Related Products'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(allow_unicode=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='product',
            name='summary',
            field=models.TextField(blank=True, null=True, verbose_name='Summary'),
        ),
        migrations.AlterField(
            model_name='product',
            name='thumbnail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='medias.image', verbose_name='Thumbnail'),
        ),
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('SIMPLE_PRODUCT', 'Simple Product'), ('VARIABLE_PRODUCT', 'Variable Product')], default='SIMPLE_PRODUCT', max_length=25, verbose_name='Product Type'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='products.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='stock',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Stock'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='stock_status',
            field=models.CharField(choices=[('IN_STOCK', 'In Stock'), ('OUT_OF_STOCK', 'Out of Stock')], default='IN_STOCK', max_length=15, verbose_name='Stock Status'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='track_inventory',
            field=models.BooleanField(default=True, verbose_name='Track Inventory'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='variables',
            field=models.ManyToManyField(blank=True, to='products.variable', verbose_name='Variables'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='variant_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='medias.image', verbose_name='Variant Image'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='color',
            field=colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=25, null=True, samples=None, verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='type',
            field=models.CharField(choices=[('LAYOUT', 'Layout'), ('SIZE', 'Size'), ('COLOR', 'Color')], default='COLOR', max_length=20, verbose_name='Variable Type'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='variant_thumbnail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medias.image', verbose_name='Variant Thumbnail'),
        ),
    ]

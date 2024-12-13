from django.db import models


class ProductType(models.TextChoices):
    """Defines different types of products in a catalog.

    - 'SIMPLE_PRODUCT': A single, standalone product.
    - 'VARIABLE_PRODUCT': A product with different variations (e.g., size, color).
    """

    SIMPLE_PRODUCT = 'SIMPLE_PRODUCT', 'Simple Product'
    VARIABLE_PRODUCT = 'VARIABLE_PRODUCT', 'Variable Product'


class StockStatus(models.TextChoices):
    """Defines the stock availability status for products.

    - 'IN_STOCK': The product is available and in stock.
    - 'OUT_OF_STOCK': The product is currently out of stock.
    """

    IN_STOCK = 'IN_STOCK', 'In Stock'
    OUT_OF_STOCK = 'OUT_OF_STOCK', 'Out of Stock'


class DiscountType(models.TextChoices):
    PERCENTAGE = 'PERCENTAGE', 'Percentage'
    CONSTANT = 'FIXED', 'Fixed'


class VariableType(models.TextChoices):
    LAYOUT = 'LAYOUT', 'Layout'
    SIZE = 'SIZE', 'Size'
    COLOR = 'COLOR', 'Color'


VariableTypeText = {
    'LAYOUT': 'طرح بندی',
    'SIZE': 'سایز بندی',
    'COLOR': 'رنگ ها'
}
